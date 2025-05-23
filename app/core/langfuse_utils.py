import os
from langfuse.callback import CallbackHandler

def init_langfuse() -> CallbackHandler:
    """
    Инициализация Langfuse для локального использования.
    """
    handler = CallbackHandler(
        host=os.getenv("LANGFUSE_URL"),
        public_key=os.getenv("LANGFUSE_INIT_PROJECT_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_INIT_PROJECT_SECRET_KEY")
    )
    handler.auth_check()
    return handler 