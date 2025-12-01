# dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session

from db.session import get_db
from rag.retrievers import get_base_retriever


def get_db_session() -> Session:
    """
    Alias wrapper so you can swap logic later if you want.
    """
    from db.session import get_db as _get_db

    return next(_get_db())  # For non-FastAPI usage


def get_retriever_dep():
    """
    FastAPI dependency for retriever, if you want it injected.
    """
    return get_base_retriever()


# For FastAPI style:
DbDep = Depends(get_db)
RetrieverDep = Depends(get_retriever_dep)
