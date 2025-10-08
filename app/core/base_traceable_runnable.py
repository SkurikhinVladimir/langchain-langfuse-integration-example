from abc import ABC, abstractmethod
from typing import TypeVar, Any, Optional, Iterator, AsyncIterator
from pydantic import ConfigDict
from langchain_core.runnables import RunnableSerializable
from langchain_core.callbacks.manager import (
    CallbackManager,
    AsyncCallbackManager,
    BaseRunManager,
)
from langchain_core.runnables.config import ensure_config, RunnableConfig
from langchain_core.runnables.base import Runnable
from langchain_core.callbacks.manager import ParentRunManager, AsyncParentRunManager

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class BaseTraceableRunnable(RunnableSerializable[InputType, OutputType], ABC):
    """
    Базовый класс для кастомных runnable с поддержкой трейсинга через Langfuse callback.
    """
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @abstractmethod
    def _run(
        self, input: InputType, *, run_manager: BaseRunManager, **kwargs: Any
    ) -> OutputType:
        """
        Основная логика runnable. Должен быть реализован в наследнике.
        """
        pass

    def invoke(
        self, input: InputType, config: Optional[RunnableConfig] = None, **kwargs: Any
    ) -> OutputType:
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
        self, input: InputType, config: Optional[RunnableConfig] = None, **kwargs: Any
    ) -> OutputType:
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
        self, input: InputType, *, run_manager: BaseRunManager, **kwargs: Any
    ) -> OutputType:
        """
        Асинхронная версия основной логики. По умолчанию вызывает sync-метод.
        """
        return self._run(input, run_manager=run_manager, **kwargs)

    def stream(
        self, input: InputType, config: Optional[RunnableConfig] = None, **kwargs: Any
    ) -> Iterator[OutputType]:
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
        chunks = []
        try:
            for chunk in self._stream(input, run_manager=run_manager, **kwargs):
                if hasattr(run_manager, "on_llm_new_token"):
                    on_token = run_manager.on_llm_new_token
                    if callable(on_token):
                        on_token(str(chunk), chunk=chunk)
                chunks.append(chunk)
                yield chunk
        except Exception as e:
            run_manager.on_chain_error(e)
            raise
        else:
            # Объединяем все чанки в итоговую строку или результат
            final_result = "".join(str(c) for c in chunks)
            run_manager.on_chain_end(final_result)

    async def astream(
        self, input: InputType, config: Optional[RunnableConfig] = None, **kwargs: Any
    ) -> AsyncIterator[OutputType]:
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
        chunks = []
        try:
            async for chunk in self._astream(input, run_manager=run_manager, **kwargs):
                if hasattr(run_manager, "on_llm_new_token"):
                    on_token = getattr(run_manager, "on_llm_new_token", None)
                    if callable(on_token):
                        await on_token(str(chunk), chunk=chunk)
                chunks.append(chunk)
                yield chunk
        except Exception as e:
            await run_manager.on_chain_error(e)
            raise
        else:
            final_result = "".join(str(c) for c in chunks)
            await run_manager.on_chain_end(final_result)

    def _stream(
        self, input: InputType, *, run_manager: BaseRunManager, **kwargs: Any
    ) -> Iterator[OutputType]:
        """
        Синхронная стриминг-логика. Должна быть реализована в наследнике.
        """
        yield self._run(input, run_manager=run_manager, **kwargs)

    async def _astream(
        self, input: InputType, *, run_manager: BaseRunManager, **kwargs: Any
    ) -> AsyncIterator[OutputType]:
        """
        Асинхронная стриминг-логика. По умолчанию вызывает sync-метод.
        """
        for chunk in self._stream(input, run_manager=run_manager, **kwargs):
            yield chunk

    def invoke_nested(
        self,
        runnable: Runnable,
        input: Any,
        run_manager: ParentRunManager,
        **kwargs: Any,
    ) -> Any:
        """
        Запускает вложенный Runnable с корректной передачей run_manager.get_child()
        для вложенного трейсинга.
        """
        config = ensure_config(
            {
                "callbacks": run_manager.get_child(),
                "run_name": runnable.__class__.__name__,
            }
        )
        return runnable.invoke(input, config=config, **kwargs)

    async def ainvoke_nested(
        self,
        runnable: Runnable,
        input: Any,
        run_manager: AsyncParentRunManager,
        **kwargs: Any,
    ) -> Any:
        config = ensure_config(
            {
                "callbacks": run_manager.get_child(),
                "run_name": runnable.__class__.__name__,
            }
        )
        return await runnable.ainvoke(input, config=config, **kwargs)

    def stream_nested(
        self,
        runnable: Runnable,
        input: Any,
        run_manager: ParentRunManager,
        **kwargs: Any,
    ) -> Iterator[Any]:
        """
        Синхронный стриминг вложенного Runnable с корректной передачей run_manager.get_child().
        """
        config = ensure_config(
            {
                "callbacks": run_manager.get_child(),
                "run_name": runnable.__class__.__name__,
            }
        )
        yield from runnable.stream(input, config=config, **kwargs)

    async def astream_nested(
        self,
        runnable: Runnable,
        input: Any,
        run_manager: AsyncParentRunManager,
        **kwargs: Any,
    ) -> AsyncIterator[Any]:
        """
        Асинхронный стриминг вложенного Runnable с корректной передачей run_manager.get_child().
        """
        config = ensure_config(
            {
                "callbacks": run_manager.get_child(),
                "run_name": runnable.__class__.__name__,
            }
        )
        async for chunk in runnable.astream(input, config=config, **kwargs):
            yield chunk
