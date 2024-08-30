import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Load environment variables from .env file
load_dotenv()

# Determine if we are in a testing environment
TESTING = os.getenv("TESTING", "0") == "1"

# Use the test database if in a testing environment, otherwise use the normal database
DATABASE_URL = os.getenv("TEST_DATABASE_URL") if TESTING else os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Dependency that provides a SQLAlchemy session to be used in the FastAPI endpoints.

    Yields:
        SessionLocal: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
