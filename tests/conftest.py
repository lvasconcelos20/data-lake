import os

import pytest

# Define variável de ambiente fictícia antes de importar configurações do app para evitar erro de validação
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app

# Usa SQLite em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(name="session")
async def session_fixture():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


from app.core.security import get_api_key


@pytest.fixture(name="client")
async def client_fixture(session: AsyncSession):
    async def get_session_override():
        return session

    async def get_api_key_override():
        return "test"

    app.dependency_overrides[get_db] = get_session_override
    app.dependency_overrides[get_api_key] = get_api_key_override

    # Usa ASGITransport para compatibilidade de comportamento httpx >= 0.28 ou ligação local robusta
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
