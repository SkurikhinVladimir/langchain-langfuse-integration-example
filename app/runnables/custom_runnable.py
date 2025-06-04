from core.base_traceable_runnable import BaseTraceableRunnable
import time
import asyncio
from pydantic import Field


class UppercaseRunnable(BaseTraceableRunnable):
    """
    Runnable, который переводит входную строку в верхний регистр.
    """

    def _run(self, input: str, *, run_manager, **kwargs) -> str:
        return input.upper()


class EchoRunnable(BaseTraceableRunnable):
    """
    Runnable, который возвращает входную строку без изменений (и поддерживает стриминг).
    """

    def _run(self, input: str, *, run_manager, **kwargs) -> str:
        return input

    async def _arun(self, input: str, *, run_manager, **kwargs) -> str:
        return input

    def _stream(self, input: str, *, run_manager, **kwargs):
        yield input

    async def _astream(self, input: str, *, run_manager, **kwargs):
        yield input


class RaiseExceptionRunnable(BaseTraceableRunnable):
    """
    Runnable, который всегда выбрасывает ValueError для тестирования ошибок.
    """

    def _run(self, input: str, *, run_manager, **kwargs) -> str:
        raise ValueError("Ошибка при запуске цепочки")


class StreamingEchoRunnable(BaseTraceableRunnable):
    """
    Runnable, который стримит входную строку по одному символу.
    """

    def _run(self, input: str, *, run_manager, **kwargs) -> str:
        # Просто возвращаем строку целиком для совместимости с абстрактным методом
        return input

    def _stream(self, input: str, *, run_manager, **kwargs):
        for char in input:
            yield char
            time.sleep(0.05)  # имитация задержки

    async def _astream(self, input: str, *, run_manager, **kwargs):
        for char in input:
            yield char
            await asyncio.sleep(0.05)


class NestedRunnable(BaseTraceableRunnable):
    """
    Runnable, который вызывает другой runnable внутри себя (например, UppercaseRunnable).
    """

    inner_runnable: BaseTraceableRunnable = Field(default_factory=UppercaseRunnable)

    def _run(self, input: str, *, run_manager, **kwargs) -> str:
        result = self.run_nested(self.inner_runnable, input, run_manager, **kwargs)
        return f"[Nested] {result}"


class NestedStreamingRunnable(BaseTraceableRunnable):
    """
    Runnable, который стримит результат другого стримингового runnable (например, StreamingEchoRunnable).
    """

    inner_runnable: BaseTraceableRunnable = Field(default_factory=StreamingEchoRunnable)

    def _stream(self, input: str, *, run_manager, **kwargs):
        yield from self.stream_nested(self.inner_runnable, input, run_manager, **kwargs)

    async def _astream(self, input: str, *, run_manager, **kwargs):
        async for chunk in self.astream_nested(
            self.inner_runnable, input, run_manager, **kwargs
        ):
            yield chunk

    def _run(self, input: str, *, run_manager, **kwargs) -> str:
        # Заглушка для совместимости с абстрактным методом
        return input
