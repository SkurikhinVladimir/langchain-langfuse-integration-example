from abc import ABC, abstractmethod
from langchain_core.runnables import RunnableSerializable
from langchain_core.callbacks.manager import CallbackManager, AsyncCallbackManager
from langchain_core.runnables.config import ensure_config

class BaseTraceableRunnable(RunnableSerializable, ABC):
    """
    Базовый класс для кастомных runnable с поддержкой трейсинга через Langfuse callback.
    """

    @abstractmethod
    def _run(self, input, *, run_manager, **kwargs):
        """
        Основная логика runnable. Должен быть реализован в наследнике.
        """
        pass

    def invoke(self, input, config=None, **kwargs):
        """
        Синхронный запуск с трейсингом.
        """
        config = ensure_config(config)
        callback_manager = CallbackManager.configure(
            config.get("callbacks"),
            None,
            verbose=kwargs.get("verbose", False),
            inheritable_tags=config.get("tags"),
        )
        run_manager = callback_manager.on_chain_start(
            None,
            input,
            name=config.get("run_name") or self.__class__.__name__,
            run_id=kwargs.pop("run_id", None),
        )
        try:
            result = self._run(input, run_manager=run_manager, **kwargs)
        except Exception as e:
            run_manager.on_chain_error(e)
            raise
        else:
            run_manager.on_chain_end(result)
            return result

    async def ainvoke(self, input, config=None, **kwargs):
        """
        Асинхронный запуск с трейсингом.
        """
        config = ensure_config(config)
        callback_manager = AsyncCallbackManager.configure(
            config.get("callbacks"),
            None,
            verbose=kwargs.get("verbose", False),
            inheritable_tags=config.get("tags"),
        )
        run_manager = await callback_manager.on_chain_start(
            None,
            input,
            name=config.get("run_name") or self.__class__.__name__,
            run_id=kwargs.pop("run_id", None),
        )
        try:
            result = await self._arun(input, run_manager=run_manager, **kwargs)
        except Exception as e:
            await run_manager.on_chain_error(e)
            raise
        else:
            await run_manager.on_chain_end(result)
            return result

    async def _arun(self, input, *, run_manager, **kwargs):
        """
        Асинхронная версия основной логики. По умолчанию вызывает sync-метод.
        """
        return self._run(input, run_manager=run_manager, **kwargs) 