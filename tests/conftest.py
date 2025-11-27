from typing import AsyncGenerator
from unittest.mock import MagicMock, patch

import pytest
from fastapi_users.password import PasswordHelper
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.database import get_async_session, Base
from src.main import app

DB_URL = "sqlite+aiosqlite:///:memory:"
async_engine = create_async_engine(url=DB_URL)
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

async def get_test_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

app.dependency_overrides[get_async_session] = get_test_async_session

@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    import src.auth.models
    import src.trade.models
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        yield

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

# @pytest.fixture(scope="session")
# def mock_user():
#     user = MagicMock()
#     user.id = 1
#     user.email = "tm@mail.ru"
#     user.is_active = True
#     return user
#
# @pytest.fixture(scope="session")
# def auth_cookies(mock_user):
#     with patch('src.auth.router.fastapi_users.current_user', return_value=mock_user):
#         print(f"MOCK USER: {mock_user}")
#         print(f"MOCK USER: {mock_user.id}")
#         return {'fastapiusersauth': 'fake'}