from abc import ABC, abstractmethod
from typing import TypeVar, Any, Optional
from langchain_core.runnables import RunnableSerializable
from langchain_core.callbacks.manager import CallbackManager, AsyncCallbackManager, BaseRunManager
from langchain_core.runnables.config import ensure_config, RunnableConfig

Input = TypeVar("Input")
Output = TypeVar("Output")

class BaseTraceableRunnable(RunnableSerializable[Input, Output], ABC):
    """
    Базовый класс для кастомных runnable с поддержкой трейсинга через Langfuse callback.
    """

    @abstractmethod
    def _run(
        self,
        input: Input,
        *,
        run_manager: BaseRunManager,
        **kwargs: Any
    ) -> Output:
        """
        Основная логика runnable. Должен быть реализован в наследнике.
        """
        pass

    def invoke(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> Output:
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

    async def ainvoke(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> Output:
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

    async def _arun(
        self,
        input: Input,
        *,
        run_manager: BaseRunManager,
        **kwargs: Any
    ) -> Output:
        """
        Асинхронная версия основной логики. По умолчанию вызывает sync-метод.
        """
        return self._run(input, run_manager=run_manager, **kwargs)

    def stream(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> Any:
        """
        Синхронный стриминг-метод с трейсингом.
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
            for chunk in self._stream(input, run_manager=run_manager, **kwargs):
                if hasattr(run_manager, "on_llm_new_token"):
                    run_manager.on_llm_new_token(str(chunk), chunk=chunk)
                yield chunk
        except Exception as e:
            run_manager.on_chain_error(e)
            raise
        else:
            run_manager.on_chain_end(None)

    async def astream(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> Any:
        """
        Асинхронный стриминг-метод с трейсингом.
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
            async for chunk in self._astream(input, run_manager=run_manager, **kwargs):
                if hasattr(run_manager, "on_llm_new_token"):
                    await run_manager.on_llm_new_token(str(chunk), chunk=chunk)
                yield chunk
        except Exception as e:
            await run_manager.on_chain_error(e)
            raise
        else:
            await run_manager.on_chain_end(None)

    def _stream(
        self,
        input: Input,
        *,
        run_manager: BaseRunManager,
        **kwargs: Any
    ) -> Any:
        """
        Синхронная стриминг-логика. Должна быть реализована в наследнике.
        """
        yield self._run(input, run_manager=run_manager, **kwargs)

    async def _astream(
        self,
        input: Input,
        *,
        run_manager: BaseRunManager,
        **kwargs: Any
    ) -> Any:
        """
        Асинхронная стриминг-логика. По умолчанию вызывает sync-метод.
        """
        for chunk in self._stream(input, run_manager=run_manager, **kwargs):
            yield chunk 