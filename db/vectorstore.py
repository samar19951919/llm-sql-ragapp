from langchain_postgres import PGVector
from app.core.configs import settings
from app.rag.embeddings import get_embeddings

def get_vectorstore():
    vs =PGVector(
        collection_name = "VECTOR_COLLECTION",
        connection_name = settings.PG_CONNECTION_STRING,
        embeddings=get_embeddings(),
        use_jsonb=True,
    )
    return vs

