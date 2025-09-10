"""Tests for API dependencies and authentication."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_current_active_user,
    get_current_superuser,
    get_current_user,
)
from app.core.security import create_access_token
from app.db.models import User


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    """Test getting current user with valid token."""
    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)

    # Create a mock user
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed",
        is_active=True,
        is_superuser=False
    )

    # Mock database result
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user
    mock_db.execute.return_value = mock_result

    # Create valid token
    token = create_access_token(subject="testuser")
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    # Test the function
    result = await get_current_user(credentials, mock_db)

    assert result == mock_user
    assert mock_db.execute.called


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    """Test getting current user with invalid token."""
    mock_db = AsyncMock(spec=AsyncSession)

    # Invalid token
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid_token")

    # Should raise HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(credentials, mock_db)

    assert exc_info.value.status_code == 401
    assert "Could not validate credentials" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_user_user_not_found():
    """Test getting current user when user doesn't exist in database."""
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock database result - user not found
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    # Create valid token for non-existent user
    token = create_access_token(subject="nonexistent")
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    # Should raise HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(credentials, mock_db)

    assert exc_info.value.status_code == 401
    assert "Could not validate credentials" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_active_user_active():
    """Test getting current active user with active user."""
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed",
        is_active=True,
        is_superuser=False
    )

    result = await get_current_active_user(mock_user)
    assert result == mock_user


@pytest.mark.asyncio
async def test_get_current_active_user_inactive():
    """Test getting current active user with inactive user."""
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed",
        is_active=False,  # Inactive user
        is_superuser=False
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_active_user(mock_user)

    assert exc_info.value.status_code == 400
    assert "Inactive user" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_superuser_valid():
    """Test getting current superuser with valid superuser."""
    mock_user = User(
        id=1,
        username="admin",
        email="admin@example.com",
        hashed_password="hashed",
        is_active=True,
        is_superuser=True  # Superuser
    )

    result = await get_current_superuser(mock_user)
    assert result == mock_user


@pytest.mark.asyncio
async def test_get_current_superuser_not_super():
    """Test getting current superuser with regular user."""
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed",
        is_active=True,
        is_superuser=False  # Not a superuser
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_superuser(mock_user)

    assert exc_info.value.status_code == 400
    assert "doesn't have enough privileges" in exc_info.value.detail
