import os
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler


def init_langfuse() -> CallbackHandler:
    """
    Инициализация Langfuse для локального использования.
    """
    # Устанавливаем переменные окружения для CallbackHandler
    os.environ["LANGFUSE_HOST"] = os.getenv("LANGFUSE_URL", "")
    os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_INIT_PROJECT_PUBLIC_KEY", "")
    os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_INIT_PROJECT_SECRET_KEY", "")
    
    # Создаем клиент для проверки подключения
    langfuse_client = Langfuse()
    langfuse_client.auth_check()
    
    # CallbackHandler автоматически использует переменные окружения
    handler = CallbackHandler()
    return handler
