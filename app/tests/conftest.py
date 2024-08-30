import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from dotenv import load_dotenv

load_dotenv()

# Set the TESTING environment variable to "1"
os.environ["TESTING"] = "1"

# Load the test database URL
DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables before tests run
Base.metadata.create_all(bind=engine)


# Define a fixture to provide a test client
@pytest.fixture(scope="module")
def client():
    def _get_test_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as c:
        yield c


# Cleanup after tests
@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    Base.metadata.drop_all(bind=engine)
