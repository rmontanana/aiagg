import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text

from app.db.base import Base, get_db
from app.main import app

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/aiagg_test"


# Event loop scope is configured in pyproject.toml to 'session'


@pytest_asyncio.fixture(scope="session")
async def engine():
    """Async engine bound to the test DB for the session."""
    eng = create_async_engine(TEST_DATABASE_URL, echo=False)
    # Create schema once
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    # Drop schema after session
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await eng.dispose()


@pytest_asyncio.fixture
async def db_connection(engine) -> AsyncGenerator[object, None]:
    """Per-test DB connection with outer transaction for isolation."""
    conn = await engine.connect()
    trans = await conn.begin()
    # Clean state for this test inside the transaction
    table_names = [t.name for t in Base.metadata.sorted_tables]
    if table_names:
        tables_csv = ", ".join(f'"{name}"' for name in table_names)
        await conn.execute(text(f"TRUNCATE {tables_csv} RESTART IDENTITY CASCADE"))
    try:
        yield conn
    finally:
        await trans.rollback()
        await conn.close()


@pytest_asyncio.fixture
async def db_session(db_connection) -> AsyncGenerator[AsyncSession, None]:
    """AsyncSession for assertions, bound to the per-test connection."""
    SessionLocal = async_sessionmaker(bind=db_connection, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_connection) -> AsyncGenerator[AsyncClient, None]:
    """HTTP client; app DB sessions share the same connection using nested transactions."""
    SessionLocal = async_sessionmaker(bind=db_connection, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with SessionLocal() as session:
            try:
                yield session
                # Don't commit here - let the outer transaction handle it
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client

    app.dependency_overrides.clear()
