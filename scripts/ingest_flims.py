# scripts/ingest_films.py

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.rag.index_builders import ingest_films


def main() -> None:
    db: Session = SessionLocal()
    try:
        print("Starting film profile ingestion...")
        count = ingest_films(db)
        print(f"Film ingestion complete. Indexed {count} film profiles.")
    finally:
        db.close()


