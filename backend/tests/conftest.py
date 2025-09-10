import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import asyncio
import os
from app.main import app
from app.db.base import Base, get_db

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/aiagg_test"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

# Test session factory
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest_asyncio.fixture
async def db_session():
    """Create a test database session."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        yield session
    
    # Clean up tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session):
    """Create a test HTTP client."""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()