from typing import Any, Optional

from langchain_core.runnables import RunnableConfig, RunnableSerializable
from pydantic import BaseModel, Field


class UppercaseRunnable(RunnableSerializable[str, str]):

    # @classmethod
    # def is_lc_serializable(cls) -> bool:
    #     return True

    # @classmethod
    # def get_lc_namespace(cls) -> list[str]:
    #     return ["custom", "uppercase"]

    def invoke(self, input: str, config: Optional[RunnableConfig] = None, **kwargs: Any) -> str:
        return self._call_with_config(lambda x: x.upper(), input, config)

    # async def ainvoke(self, input: str, config: Optional[RunnableConfig] = None, **kwargs: Any) -> str:
    #     return await self._acall_with_config(lambda x: x.upper(), input, config)


class PassThroughRunnable(RunnableSerializable[str, str]):
    @classmethod
    def is_lc_serializable(cls) -> bool:
        return True

    @classmethod
    def get_lc_namespace(cls) -> list[str]:
        return ["custom", "pass_through"]
    
    def invoke(self, input: str, config: Optional[RunnableConfig] = None, **kwargs: Any) -> str:
        return input

    async def ainvoke(self, input: str, config: Optional[RunnableConfig] = None, **kwargs: Any) -> str:
        return input
    

class RaiseExceptionRunnable(RunnableSerializable[str, str]):
    
    def raise_value_error(self):
        raise ValueError('Ошибка при запуске цепочки')
    
    def invoke(self, input: str, config: Optional[RunnableConfig] = None, **kwargs: Any) -> str:
        return self._call_with_config(
            lambda x: self.raise_value_error(),  
            input, 
            config
        )
