import pytest
from httpx import AsyncClient
from app.core.security import get_password_hash, verify_password


@pytest.mark.asyncio
async def test_user_registration(client: AsyncClient):
    """Test user registration."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    
    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert data["is_active"] is True
    assert "password" not in data


@pytest.mark.asyncio
async def test_user_login(client: AsyncClient):
    """Test user login."""
    # First register a user
    user_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "loginpassword123"
    }
    await client.post("/auth/register", json=user_data)
    
    # Then try to login
    login_data = {
        "username": "loginuser",
        "password": "loginpassword123"
    }
    
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_duplicate_user_registration(client: AsyncClient):
    """Test duplicate user registration fails."""
    user_data = {
        "email": "duplicate@example.com",
        "username": "duplicate",
        "password": "password123"
    }
    
    # Register first user
    response1 = await client.post("/auth/register", json=user_data)
    assert response1.status_code == 200
    
    # Try to register duplicate user
    response2 = await client.post("/auth/register", json=user_data)
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"]


def test_password_hashing():
    """Test password hashing functionality."""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False