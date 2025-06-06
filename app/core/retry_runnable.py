from .base_traceable_runnable import BaseTraceableRunnable
from pydantic import Field
import time
import asyncio

class RetryRunnable(BaseTraceableRunnable):
    """
    Runnable, который повторяет попытку вызова внутреннего runnable при ошибке.
    """
    inner_runnable: BaseTraceableRunnable = Field(...)
    max_retries: int = Field(default=1)
    delay: float = Field(default=0)  # в секундах

    def _run(self, input: str, *, run_manager, **kwargs) -> str:
        last_exc = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return self.invoke_nested(self.inner_runnable, input, run_manager, **kwargs)
            except Exception as exc:
                last_exc = exc
                if attempt < self.max_retries:
                    time.sleep(self.delay)
        if last_exc is not None:
            raise last_exc
        else:
            raise RuntimeError("Unknown error in RetryRunnable")

    async def _arun(self, input: str, *, run_manager, **kwargs) -> str:
        last_exc = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return await self.ainvoke_nested(self.inner_runnable, input, run_manager, **kwargs)
            except Exception as exc:
                last_exc = exc
                if attempt < self.max_retries:
                    await asyncio.sleep(self.delay)
        if last_exc is not None:
            raise last_exc
        else:
            raise RuntimeError("Unknown error in RetryRunnable") 