from .base_traceable_runnable import BaseTraceableRunnable
from pydantic import Field
import time
import asyncio
from typing import Optional

class RetryRunnable(BaseTraceableRunnable):
    """
    Runnable, который повторяет попытку вызова внутреннего runnable при ошибке.
    """
    inner_runnable: BaseTraceableRunnable = Field(...)
    max_retries: int = Field(default=1)
    delay: float = Field(default=0)  # в секундах
    default_value: Optional[str] = Field(default=None)

    def _handle_final_result(self, last_exc):
        if self.default_value is not None:
            return self.default_value
        if last_exc is not None:
            raise last_exc
        else:
            raise RuntimeError("Unknown error in RetryRunnable")

    def _run(self, input: str, *, run_manager, **kwargs) -> str:
        last_exc = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return self.invoke_nested(self.inner_runnable, input, run_manager, **kwargs)
            except Exception as exc:
                last_exc = exc
                if attempt < self.max_retries:
                    time.sleep(self.delay)
        return self._handle_final_result(last_exc)

    async def _arun(self, input: str, *, run_manager, **kwargs) -> str:
        last_exc = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return await self.ainvoke_nested(self.inner_runnable, input, run_manager, **kwargs)
            except Exception as exc:
                last_exc = exc
                if attempt < self.max_retries:
                    await asyncio.sleep(self.delay)
        return self._handle_final_result(last_exc)

    def _stream(self, input: str, *, run_manager, **kwargs) -> Iterator[str]:
        last_exc = None
        for attempt in range(1, self.max_retries + 1):
            try:
                yield from self.stream_nested(self.inner_runnable, input, run_manager, **kwargs)
                return
            except Exception as exc:
                last_exc = exc
                if attempt < self.max_retries:
                    time.sleep(self.delay)
        
        result = self._handle_final_result(last_exc)
        if result is not None:
            yield result

    async def _astream(self, input: str, *, run_manager, **kwargs) -> AsyncIterator[str]:
        last_exc = None
        for attempt in range(1, self.max_retries + 1):
            try:
                async for chunk in self.astream_nested(self.inner_runnable, input, run_manager, **kwargs):
                    yield chunk
                return
            except Exception as exc:
                last_exc = exc
                if attempt < self.max_retries:
                    await asyncio.sleep(self.delay)
        
        result = self._handle_final_result(last_exc)
        if result is not None:
            yield result
