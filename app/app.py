import os
from typing import Any, Dict, List, Optional

from custom_runnable import (PassThroughRunnable, RaiseExceptionRunnable,
                             UppercaseRunnable)
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.schema import StrOutputParser
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.config import RunnableConfig
from langfuse.callback import CallbackHandler
from langserve import add_routes

load_dotenv()


def init_langfuse():
    """Инициализация Langfuse для локального использования"""
    handler = CallbackHandler(
        host=os.getenv("LANGFUSE_URL"),
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
    | PassThroughRunnable()
    | UppercaseRunnable()
).with_config(config)


chain_with_error = (
    prompt 
    | llm 
    | StrOutputParser()
    | PassThroughRunnable()
    | UppercaseRunnable()
    | RaiseExceptionRunnable()
).with_config(config)


# Настройка сервера
app = FastAPI(
    title="Langfuse Integration Example",
    description="Пример интеграции Langfuse с LangChain",
    version="1.0.0"
)

# Добавление маршрута Langserve с моделями
add_routes(
    app,
    chain,
    path="/v1",
    enabled_endpoints=["invoke"]
)

add_routes(
    app,
    chain_with_error,
    path="/v2",
    enabled_endpoints=["invoke"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
