import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv(override=True)
DATABASE_URL=os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) # Datasource

session = sessionmaker( # EntityManagerFactory OR session factory.
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base = declarative_base() # Base class for our models. It maintains a catalog of classes and tables relative to that base.
Base = declarative_base()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
    return db






