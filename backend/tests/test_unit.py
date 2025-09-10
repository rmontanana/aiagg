"""Unit tests that don't require database connection."""

import pytest
from app.core.security import get_password_hash, verify_password, create_access_token, verify_token


def test_password_hashing():
    """Test password hashing functionality."""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_jwt_token_creation_and_verification():
    """Test JWT token creation and verification."""
    test_subject = "testuser"
    
    # Create token
    token = create_access_token(subject=test_subject)
    assert token is not None
    assert isinstance(token, str)
    
    # Verify token
    verified_subject = verify_token(token)
    assert verified_subject == test_subject


def test_jwt_token_invalid():
    """Test invalid JWT token handling."""
    invalid_token = "invalid.token.here"
    result = verify_token(invalid_token)
    assert result is None


def test_settings_loading():
    """Test that settings load correctly."""
    from app.core.config import settings
    
    assert settings.PROJECT_NAME == "AI News Aggregator"
    assert settings.VERSION == "1.0.0"
    assert settings.ALGORITHM == "HS256"