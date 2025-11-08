import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from src.auth.models import User
from src.conf import settings
from src.database import Base, get_async_session, async_session
from src.main import app


TEST_DB = settings.DB_TEST_URL

@pytest.fixture(scope="function")
async def test_db():
    engine = create_engine(
        TEST_DB,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Create all tables
    Base.metadata.create_all(bind=engine)
    # Create test session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Get test session
    def get_test_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_async_session] = get_test_db

    yield engine

    app.dependency_overrides.clear()

@pytest.fixture
def test_client(test_db):
    # Fixture test client FastAPI
    with TestClient(app) as client:
        yield client

@pytest.fixture
async def test_user(test_db):
    # Fixture test user
    from src.auth.utilits import get_password_hash

    async with async_session() as session:
        user = User(
            email="testuser@example.com",
            hashed_password=get_password_hash("string"),
            username="testuser"
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user