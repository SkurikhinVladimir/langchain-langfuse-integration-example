from langchain.schema import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.config import RunnableConfig
from runnables.llm_stub import SimpleLLM
from runnables.custom_runnable import (
    EchoRunnable,
    UppercaseRunnable,
    RaiseExceptionRunnable,
    StreamingEchoRunnable,
    NestedRunnable,
    NestedStreamingRunnable,
)
from core.retry_runnable import RetryRunnable


def get_prompt():
    return ChatPromptTemplate.from_messages(
        [("system", "Ты - полезный ассистент"), ("human", "{input}")]
    )


def create_chain(config: RunnableConfig):
    prompt = get_prompt()
    llm = SimpleLLM()
    return (
        prompt | llm | StrOutputParser() | EchoRunnable() | UppercaseRunnable()
    ).with_config(config)


def create_chain_with_error(config: RunnableConfig):
    prompt = get_prompt()
    llm = SimpleLLM()
    return (
        prompt
        | llm
        | StrOutputParser()
        | EchoRunnable()
        | UppercaseRunnable()
        | RaiseExceptionRunnable()
    ).with_config(config)


def create_streaming_chain(config: RunnableConfig):
    prompt = get_prompt()
    llm = SimpleLLM()
    return (
        prompt | llm | StrOutputParser() | EchoRunnable() | StreamingEchoRunnable()
    ).with_config(config)


def create_nested_chain(config: RunnableConfig):
    prompt = get_prompt()
    llm = SimpleLLM()
    return (
        prompt | llm | StrOutputParser() | EchoRunnable() | NestedRunnable()
    ).with_config(config)


def create_nested_streaming_chain(config: RunnableConfig):
    prompt = get_prompt()
    llm = SimpleLLM()
    return (
        prompt | llm | StrOutputParser() | EchoRunnable() | NestedStreamingRunnable()
    ).with_config(config)


def create_retry_chain(config: RunnableConfig):
    prompt = get_prompt()
    llm = SimpleLLM()
    retry_runnable: RetryRunnable = RetryRunnable(
        inner_runnable=RaiseExceptionRunnable(),
        max_retries=3,
        delay=0.1,
    )
    return (
        prompt | llm | StrOutputParser() | EchoRunnable() | retry_runnable
    ).with_config(config)
