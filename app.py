import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.runnables.config import RunnableConfig
from langfuse.callback import CallbackHandler
from langserve import add_routes
from langchain.schema import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

def init_langfuse():
    """Инициализация Langfuse для локального использования"""
    handler = CallbackHandler(
        host="http://localhost:3000",
        public_key=os.getenv("LANGFUSE_INIT_PROJECT_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_INIT_PROJECT_SECRET_KEY")
    )
    # Проверка подключения к серверу
    handler.auth_check()
    return handler

class SimpleLLM(BaseChatModel):
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


# Инициализация компонентов
langfuse_handler = init_langfuse()
llm = SimpleLLM()
config = RunnableConfig(callbacks=[langfuse_handler])

prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты - полезный ассистент"),
    ("human", "{input}")
])

chain = (
    prompt 
    | llm 
    | StrOutputParser()
).with_config(config)

# Настройка сервера
app = FastAPI()

# Добавление маршрута Langserve
add_routes(
    app,
    chain,
    path="/test-simple-llm-call",
)

chain.invoke({"input": "Hello, world!"})