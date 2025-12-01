from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from app.core.configs import settings


#creating the database engine

engine = create_engine(settings.PG_CONNECTION_STRING,
                       
                        pool_pre_ping=True)



#creating the sesion local areas

SessionLocal = sessionmaker(autocommit = False,
                            
                             autoflush=False, 

                             bind=engine)


#Base class for ORM models

Base  = declarative_base()


#defing the function to get the db sesssion

def get_db():
    db  = SessionLocal()
    try:
        yield db
    
    finally:
        db.close()