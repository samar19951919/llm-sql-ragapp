# scripts/ingest_customers.py

from sqlalchemy.orm import Session

from db.session import SessionLocal
from rag.index_builders import ingest_customers


def main() -> None:
    db: Session = SessionLocal()
    try:
        print("Starting customer profile ingestion...")
        count = ingest_customers(db)
        print(f"Customer ingestion complete. Indexed {count} customer profiles.")
    finally:
        db.close()



