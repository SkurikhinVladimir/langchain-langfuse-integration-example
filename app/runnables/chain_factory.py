from langchain.schema import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.config import RunnableConfig
from runnables.llm_stub import SimpleLLM
from runnables.custom_runnable import PassThroughRunnable, UppercaseRunnable, RaiseExceptionRunnable, StreamingEchoRunnable

def get_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "Ты - полезный ассистент"),
        ("human", "{input}")
    ])

def create_chain(config: RunnableConfig):
    prompt = get_prompt()
    llm = SimpleLLM()
    return (
        prompt
        | llm
        | StrOutputParser()
        | PassThroughRunnable()
        | UppercaseRunnable()
    ).with_config(config)

def create_chain_with_error(config: RunnableConfig):
    prompt = get_prompt()
    llm = SimpleLLM()
    return (
        prompt
        | llm
        | StrOutputParser()
        | PassThroughRunnable()
        | UppercaseRunnable()
        | RaiseExceptionRunnable()
    ).with_config(config)

def create_streaming_chain(config: RunnableConfig):
    prompt = get_prompt()
    llm = SimpleLLM()
    return (
        prompt
        | llm
        | StrOutputParser()
        | PassThroughRunnable()
        | StreamingEchoRunnable()
    ).with_config(config) 