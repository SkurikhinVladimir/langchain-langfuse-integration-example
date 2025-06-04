from typing import Any, Dict, List, Optional
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult


class SimpleLLM(BaseChatModel):
    """
    Простая LLM-заглушка для демонстрации работы цепочек.
    """

    model_name: str = "simple-llm"
    temperature: float = 0.7

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        last_message = messages[-1].content if messages else ""
        res = f"🤖 Я получил ваше сообщение: '{last_message}'\n\n✨ Спасибо за использование! 🎉"
        message = AIMessage(content=res)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "simple"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {"model_name": self.model_name, "temperature": self.temperature}
