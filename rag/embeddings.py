# in this we are getting the embedding model in the system
from langchain_openai import OpenAIEmbeddings

from core.configs import settings


def get_embeddings():
    """Return the configured embedding model instance."""

    return OpenAIEmbeddings(model=settings.EMBEDDING_MODEL)
