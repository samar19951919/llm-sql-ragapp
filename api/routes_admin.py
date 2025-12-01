# app/api/routes_admin.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.rag.index_builders import (
    ingest_customers,
    ingest_films,
    ingest_actors,
    ingest_all_profiles,
)
from app.schemas.admin import (
    ReindexEntityResponse,
    ReindexProfilesResponse,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/reindex/customers", response_model=ReindexEntityResponse)
def reindex_customers(db: Session = Depends(get_db)) -> ReindexEntityResponse:
    """
    Trigger ingestion of customer profile docs into pgvector.
    """
    count = ingest_customers(db)
    return ReindexEntityResponse(indexed_count=count)


@router.post("/reindex/films", response_model=ReindexEntityResponse)
def reindex_films(db: Session = Depends(get_db)) -> ReindexEntityResponse:
    """
    Trigger ingestion of film profile docs into pgvector.
    """
    count = ingest_films(db)
    return ReindexEntityResponse(indexed_count=count)


@router.post("/reindex/actors", response_model=ReindexEntityResponse)
def reindex_actors(db: Session = Depends(get_db)) -> ReindexEntityResponse:
    """
    Trigger ingestion of actor profile docs into pgvector.
    """
    count = ingest_actors(db)
    return ReindexEntityResponse(indexed_count=count)


@router.post("/reindex/all", response_model=ReindexProfilesResponse)
def reindex_all_profiles_endpoint(
    db: Session = Depends(get_db),
) -> ReindexProfilesResponse:
    """
    Trigger ingestion of ALL profile docs:
    - customers
    - films
    - actors
    """
    counts = ingest_all_profiles(db)
    return ReindexProfilesResponse(
        customers_indexed=counts["customers_indexed"],
        films_indexed=counts["films_indexed"],
        actors_indexed=counts["actors_indexed"],
    )
