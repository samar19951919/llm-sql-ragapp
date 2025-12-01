from langchain_openai import ChatOpenAI

from core.configs import settings


# now getting the chat model to display in the system.

def get_chat_model() -> ChatOpenAI:
    # now defining the chat model
    return ChatOpenAI(
        model=settings.CHAT_MODEL,
        temperature=0.4,
    )
