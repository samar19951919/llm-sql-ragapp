from langchain_postgres import PGVector

from core.configs import settings
from rag.embeddings import get_embeddings


def get_vectorstore() -> PGVector:
    """Create a PGVector instance configured from settings."""

    return PGVector(
        collection_name=settings.VECTOR_COLLECTION,
        connection_string=settings.PG_CONNECTION_STRING,
        embeddings=get_embeddings(),
        use_jsonb=True,
    )
