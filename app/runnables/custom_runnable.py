from typing import Any, Optional
from core.base_traceable_runnable import BaseTraceableRunnable
import time
import asyncio

class UppercaseRunnable(BaseTraceableRunnable):
    """
    Runnable, который переводит входную строку в верхний регистр.
    """
    def _run(self, input: str, *, run_manager, **kwargs) -> str:
        return input.upper()

class PassThroughRunnable(BaseTraceableRunnable):
    """
    Runnable, который возвращает входную строку без изменений.
    """
    def _run(self, input: str, *, run_manager, **kwargs) -> str:
        return input

    async def _arun(self, input: str, *, run_manager, **kwargs) -> str:
        return input

class RaiseExceptionRunnable(BaseTraceableRunnable):
    """
    Runnable, который всегда выбрасывает ValueError для тестирования ошибок.
    """
    def _run(self, input: str, *, run_manager, **kwargs) -> str:
        raise ValueError('Ошибка при запуске цепочки')

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
