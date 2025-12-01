# in this we are getting the embedding model in the system
from langchain_openai import OpenAIEmbeddings

from app.core.configs import settings


def get_embeddings():
    " here we are getting the embeddung which we placed in the above model"

    return OpenAIEmbeddings(model = settings.EMBEDDING_MODEL)


