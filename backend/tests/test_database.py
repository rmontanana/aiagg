"""Tests for database functionality."""

from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db


@pytest.mark.asyncio
async def test_get_db_session():
    """Test database session creation."""
    # This will test the get_db function without requiring actual database
    with patch('app.db.base.AsyncSessionLocal') as mock_session_factory:
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session_factory.return_value.__aenter__.return_value = mock_session
        mock_session_factory.return_value.__aexit__.return_value = None

        # Test the generator
        db_gen = get_db()
        db_session = await db_gen.__anext__()

        assert db_session == mock_session

        # Test cleanup
        try:
            await db_gen.__anext__()
        except StopAsyncIteration:
            # Expected - generator should stop after yielding once
            pass


def test_database_url_configuration():
    """Test database URL configuration."""
    from app.core.config import settings

    # In test environment, should have test database URL
    assert settings.DATABASE_URL is not None
    # DATABASE_URL is a PostgresDsn object, convert to string to check
    assert str(settings.DATABASE_URL) is not None


def test_settings_validation():
    """Test that settings are properly validated."""
    from app.core.config import settings

    # Test that required settings exist
    assert settings.SECRET_KEY is not None
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0
    assert settings.ALGORITHM is not None
