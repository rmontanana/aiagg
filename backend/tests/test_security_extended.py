"""Extended security tests for 100% coverage."""

from datetime import timedelta

from jose import jwt

from app.core.config import settings
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    verify_token,
)


def test_create_access_token_with_custom_expiry():
    """Test access token creation with custom expiry time."""
    test_subject = "testuser"
    custom_expires = timedelta(minutes=60)

    token = create_access_token(subject=test_subject, expires_delta=custom_expires)

    # Verify token can be decoded
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == test_subject
    assert "exp" in payload


def test_verify_token_invalid():
    """Test token verification with invalid token."""
    invalid_token = "invalid.token.here"
    result = verify_token(invalid_token)
    assert result is None


def test_verify_token_malformed():
    """Test token verification with malformed token."""
    malformed_token = "not-a-jwt-token"
    result = verify_token(malformed_token)
    assert result is None


def test_verify_token_wrong_secret():
    """Test token verification with wrong secret."""
    # Create token with different secret
    payload = {"sub": "testuser", "exp": 9999999999}
    wrong_token = jwt.encode(payload, "wrong-secret", algorithm=settings.ALGORITHM)

    result = verify_token(wrong_token)
    assert result is None


def test_password_verification_mismatch():
    """Test password verification with wrong password."""
    password = "correct_password"
    wrong_password = "wrong_password"
    hashed = get_password_hash(password)

    assert verify_password(wrong_password, hashed) is False


def test_password_hashing_different_passwords():
    """Test that different passwords produce different hashes."""
    password1 = "password1"
    password2 = "password2"

    hash1 = get_password_hash(password1)
    hash2 = get_password_hash(password2)

    assert hash1 != hash2
    assert verify_password(password1, hash1) is True
    assert verify_password(password2, hash2) is True
    assert verify_password(password1, hash2) is False
