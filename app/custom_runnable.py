from langchain_core.runnables import RunnableSerializable, RunnableConfig
from typing import Optional
from typing import Any
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

    async def ainvoke(self, input: str, config: Optional[RunnableConfig] = None, **kwargs: Any) -> str:
        return await self._acall_with_config(lambda x: x.upper(), input, config)


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
    
    def get_input_schema(self, config: Optional[RunnableConfig] = None) -> type[BaseModel]:
        """Возвращает схему входных данных."""
        return str
    
    def get_output_schema(self, config: Optional[RunnableConfig] = None) -> type[BaseModel]:
        """Возвращает схему выходных данных."""
        return str

