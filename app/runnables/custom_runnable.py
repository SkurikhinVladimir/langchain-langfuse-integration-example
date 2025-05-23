from typing import Any, Optional
from core.base_traceable_runnable import BaseTraceableRunnable

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
