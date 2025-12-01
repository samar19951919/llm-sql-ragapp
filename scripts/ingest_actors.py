# scripts/ingest_actors.py

from sqlalchemy.orm import Session

from db.session import SessionLocal
from rag.index_builders import ingest_actors


def main() -> None:
    db: Session = SessionLocal()
    try:
        print("Starting actor profile ingestion...")
        count = ingest_actors(db)
        print(f"Actor ingestion complete. Indexed {count} actor profiles.")
    finally:
        db.close()


