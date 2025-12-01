from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.configs import settings

# creating the database engine
engine = create_engine(
    settings.PG_CONNECTION_STRING,
    pool_pre_ping=True,
)

# creating the session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for ORM models
Base = declarative_base()


# defining the function to get the db session
# (FastAPI dependency generator style)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
