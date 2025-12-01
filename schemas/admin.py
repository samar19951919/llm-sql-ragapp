# app/schemas/admin.py
# app/schemas/admin.py

from pydantic import BaseModel


class ReindexEntityResponse(BaseModel):
    """
    Response model when reindexing a single entity type
    (customers, films, or actors).
    """
    indexed_count: int


class ReindexProfilesResponse(BaseModel):
    """
    Response model when reindexing all profiles at once.
    """
    customers_indexed: int
    films_indexed: int
    actors_indexed: int

