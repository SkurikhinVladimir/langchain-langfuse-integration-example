from fastapi import FastAPI
from langchain_core.runnables.config import RunnableConfig
from langserve import add_routes

from core.langfuse_utils import init_langfuse
from runnables.chain_factory import (
    create_chain,
    create_chain_with_error,
    create_streaming_chain,
    create_nested_chain,
    create_nested_streaming_chain,
    create_retry_chain,
)

# Инициализация Langfuse handler и конфиг для runnable
langfuse_handler = init_langfuse()
config = RunnableConfig(callbacks=[langfuse_handler])

# Создание цепочек
chain = create_chain(config)
chain_with_error = create_chain_with_error(config)
streaming_chain = create_streaming_chain(config)
nested_chain = create_nested_chain(config)
nested_streaming_chain = create_nested_streaming_chain(config)
retry_chain = create_retry_chain(config)

# FastAPI приложение
app = FastAPI(
    title="LangServe + Langfuse Demo",
    description="Демонстрация интеграции LangServe, кастомных runnable и Langfuse",
    version="1.0.0",
)

# Endpoint обычной цепочки
add_routes(app, chain, path="/v1", enabled_endpoints=["invoke"])

# Endpoint цепочки с ошибкой
add_routes(app, chain_with_error, path="/v2", enabled_endpoints=["invoke"])

# Endpoint стриминговой цепочки
add_routes(app, streaming_chain, path="/v3", enabled_endpoints=["invoke", "stream"])

# Endpoint цепочки с вложенным runnable
add_routes(app, nested_chain, path="/v4", enabled_endpoints=["invoke"])

# Endpoint для вложенного стриминга
add_routes(
    app, nested_streaming_chain, path="/v5", enabled_endpoints=["invoke", "stream"]
)
# Endpoint для RetryRunnable chain
add_routes(app, retry_chain, path="/v6", enabled_endpoints=["invoke", "stream"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
