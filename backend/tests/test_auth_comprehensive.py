"""Comprehensive authentication tests covering all functionality."""
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import User
from app.core.security import verify_password, get_password_hash


@pytest.fixture
def valid_user_data():
    """Valid user registration data."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }


class TestUserRegistration:
    """Test user registration functionality."""

    @pytest.mark.asyncio
    async def test_successful_registration(self, client: AsyncClient, db_session: AsyncSession, valid_user_data):
        """Test successful user registration."""
        response = await client.post("/auth/register", json=valid_user_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response data
        assert data["email"] == valid_user_data["email"]
        assert data["username"] == valid_user_data["username"]
        assert data["is_active"] is True
        assert "id" in data
        assert "password" not in data  # Password should not be returned
        
        # Verify user was created in database
        result = await db_session.execute(
            select(User).where(User.email == valid_user_data["email"])
        )
        user = result.scalar_one_or_none()
        assert user is not None
        assert user.email == valid_user_data["email"]
        assert user.username == valid_user_data["username"]
        assert user.is_active is True
        assert verify_password(valid_user_data["password"], user.hashed_password)

    async def test_registration_duplicate_email(self, client: AsyncClient, db_session: AsyncSession, valid_user_data):
        """Test registration with duplicate email."""
        # Register first user
        await client.post("/auth/register", json=valid_user_data)
        
        # Try to register with same email but different username
        duplicate_data = valid_user_data.copy()
        duplicate_data["username"] = "differentuser"
        
        response = await client.post("/auth/register", json=duplicate_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "Email or username already registered" in data["detail"]

    async def test_registration_duplicate_username(self, client: AsyncClient, db_session: AsyncSession, valid_user_data):
        """Test registration with duplicate username."""
        # Register first user
        await client.post("/auth/register", json=valid_user_data)
        
        # Try to register with same username but different email
        duplicate_data = valid_user_data.copy()
        duplicate_data["email"] = "different@example.com"
        
        response = await client.post("/auth/register", json=duplicate_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "Email or username already registered" in data["detail"]

    async def test_registration_missing_email(self, client: AsyncClient):
        """Test registration with missing email field."""
        invalid_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        
        response = await client.post("/auth/register", json=invalid_data)
        
        assert response.status_code == 422
        data = response.json()
        assert any(error["loc"] == ["body", "email"] for error in data["detail"])
        assert any("Field required" in error["msg"] for error in data["detail"])

    async def test_registration_missing_username(self, client: AsyncClient):
        """Test registration with missing username field."""
        invalid_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = await client.post("/auth/register", json=invalid_data)
        
        assert response.status_code == 422
        data = response.json()
        assert any(error["loc"] == ["body", "username"] for error in data["detail"])
        assert any("Field required" in error["msg"] for error in data["detail"])

    async def test_registration_missing_password(self, client: AsyncClient):
        """Test registration with missing password field."""
        invalid_data = {
            "email": "test@example.com",
            "username": "testuser"
        }
        
        response = await client.post("/auth/register", json=invalid_data)
        
        assert response.status_code == 422
        data = response.json()
        assert any(error["loc"] == ["body", "password"] for error in data["detail"])
        assert any("Field required" in error["msg"] for error in data["detail"])

    async def test_registration_invalid_email_format(self, client: AsyncClient):
        """Test registration with invalid email format."""
        invalid_data = {
            "email": "invalidemail",
            "username": "testuser",
            "password": "testpassword123"
        }
        
        response = await client.post("/auth/register", json=invalid_data)
        
        assert response.status_code == 422
        data = response.json()
        assert any(error["loc"] == ["body", "email"] for error in data["detail"])
        assert any("email address" in error["msg"].lower() for error in data["detail"])

    @pytest.mark.parametrize("invalid_email", [
        "no-at-sign",
        "@missing-local.com",
        "missing-domain@",
        "spaces @domain.com",
        "multiple@@domain.com"
    ])
    async def test_registration_various_invalid_email_formats(self, client: AsyncClient, invalid_email):
        """Test registration with various invalid email formats."""
        invalid_data = {
            "email": invalid_email,
            "username": "testuser",
            "password": "testpassword123"
        }
        
        response = await client.post("/auth/register", json=invalid_data)
        assert response.status_code == 422

    async def test_registration_empty_fields(self, client: AsyncClient):
        """Test registration with empty string fields."""
        invalid_data = {
            "email": "",
            "username": "",
            "password": ""
        }
        
        response = await client.post("/auth/register", json=invalid_data)
        assert response.status_code == 422

    async def test_registration_whitespace_fields(self, client: AsyncClient):
        """Test registration with whitespace-only fields."""
        invalid_data = {
            "email": "   ",
            "username": "   ",
            "password": "   "
        }
        
        response = await client.post("/auth/register", json=invalid_data)
        assert response.status_code == 422

    async def test_registration_no_request_body(self, client: AsyncClient):
        """Test registration with no request body."""
        response = await client.post("/auth/register")
        assert response.status_code == 422

    async def test_registration_wrong_content_type(self, client: AsyncClient):
        """Test registration with wrong content type."""
        data = "email=test@example.com&username=testuser&password=test123"
        response = await client.post("/auth/register", content=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        assert response.status_code == 422


class TestUserLogin:
    """Test user login functionality."""

    @pytest.fixture
    def registered_user_data(self):
        """Data for a user that will be registered for testing."""
        return {
            "email": "login@example.com",
            "username": "loginuser",
            "password": "loginpassword123"
        }

    @pytest_asyncio.fixture
    async def registered_user(self, client: AsyncClient, registered_user_data):
        """Create a registered user for login tests."""
        await client.post("/auth/register", json=registered_user_data)
        return registered_user_data

    async def test_successful_login_with_username(self, client: AsyncClient, registered_user):
        """Test successful login with username."""
        login_data = {
            "username": registered_user["username"],
            "password": registered_user["password"]
        }
        
        response = await client.post(
            "/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check token structure
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0
        
        # JWT tokens have 3 parts separated by dots
        token_parts = data["access_token"].split(".")
        assert len(token_parts) == 3

    async def test_login_invalid_username(self, client: AsyncClient, registered_user):
        """Test login with invalid username."""
        login_data = {
            "username": "nonexistentuser",
            "password": registered_user["password"]
        }
        
        response = await client.post(
            "/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Incorrect username or password" in data["detail"]

    async def test_login_invalid_password(self, client: AsyncClient, registered_user):
        """Test login with invalid password."""
        login_data = {
            "username": registered_user["username"],
            "password": "wrongpassword"
        }
        
        response = await client.post(
            "/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Incorrect username or password" in data["detail"]

    async def test_login_with_email_as_username(self, client: AsyncClient, registered_user):
        """Test that login with email in username field fails (username-only login)."""
        login_data = {
            "username": registered_user["email"],
            "password": registered_user["password"]
        }
        
        response = await client.post(
            "/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Incorrect username or password" in data["detail"]

    async def test_login_missing_username(self, client: AsyncClient):
        """Test login with missing username."""
        login_data = {
            "password": "somepassword"
        }
        
        response = await client.post(
            "/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 422
        data = response.json()
        assert any(error["loc"] == ["body", "username"] for error in data["detail"])

    async def test_login_missing_password(self, client: AsyncClient):
        """Test login with missing password."""
        login_data = {
            "username": "testuser"
        }
        
        response = await client.post(
            "/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 422
        data = response.json()
        assert any(error["loc"] == ["body", "password"] for error in data["detail"])

    async def test_login_empty_fields(self, client: AsyncClient):
        """Test login with empty fields."""
        login_data = {
            "username": "",
            "password": ""
        }
        
        response = await client.post(
            "/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # OAuth2PasswordRequestForm returns 400 for empty credentials, not 422
        assert response.status_code == 400

    async def test_login_wrong_content_type(self, client: AsyncClient, registered_user):
        """Test login with JSON instead of form data."""
        login_data = {
            "username": registered_user["username"],
            "password": registered_user["password"]
        }
        
        response = await client.post("/auth/login", json=login_data)
        assert response.status_code == 422

    async def test_login_no_request_body(self, client: AsyncClient):
        """Test login with no request body."""
        response = await client.post("/auth/login")
        assert response.status_code == 422

    async def test_multiple_successful_logins(self, client: AsyncClient, registered_user):
        """Test that multiple logins work and return valid tokens."""
        import asyncio
        
        login_data = {
            "username": registered_user["username"],
            "password": registered_user["password"]
        }
        
        # First login
        response1 = await client.post(
            "/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # Small delay to ensure different timestamps
        await asyncio.sleep(0.1)
        
        # Second login
        response2 = await client.post(
            "/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        token1 = response1.json()["access_token"]
        token2 = response2.json()["access_token"]
        
        # Both tokens should be valid JWT format
        assert len(token1.split(".")) == 3
        assert len(token2.split(".")) == 3
        assert isinstance(token1, str) and len(token1) > 0
        assert isinstance(token2, str) and len(token2) > 0
        
        # Multiple logins should work (tokens might be identical if generated within same minute)


class TestDatabaseIntegration:
    """Test database integration for authentication."""

    async def test_user_password_hashing(self, client: AsyncClient, db_session: AsyncSession):
        """Test that passwords are properly hashed in the database."""
        user_data = {
            "email": "hash@example.com",
            "username": "hashuser",
            "password": "plaintext123"
        }
        
        await client.post("/auth/register", json=user_data)
        
        # Get user from database
        result = await db_session.execute(
            select(User).where(User.username == user_data["username"])
        )
        user = result.scalar_one()
        
        # Password should be hashed, not stored as plaintext
        assert user.hashed_password != user_data["password"]
        assert len(user.hashed_password) > len(user_data["password"])
        assert user.hashed_password.startswith("$")  # bcrypt hash format
        
        # Verify password verification works
        assert verify_password(user_data["password"], user.hashed_password)
        assert not verify_password("wrongpassword", user.hashed_password)

    async def test_user_creation_timestamps(self, client: AsyncClient, db_session: AsyncSession):
        """Test that user creation and update timestamps are set."""
        user_data = {
            "email": "timestamp@example.com",
            "username": "timestampuser",
            "password": "test123"
        }
        
        await client.post("/auth/register", json=user_data)
        
        # Get user from database
        result = await db_session.execute(
            select(User).where(User.username == user_data["username"])
        )
        user = result.scalar_one()
        
        assert user.created_at is not None
        assert user.updated_at is not None
        # For new users, created_at and updated_at should be very close
        time_diff = user.updated_at - user.created_at
        assert time_diff.total_seconds() < 1.0

    async def test_user_default_values(self, client: AsyncClient, db_session: AsyncSession):
        """Test that users have correct default values."""
        user_data = {
            "email": "defaults@example.com",
            "username": "defaultuser",
            "password": "test123"
        }
        
        await client.post("/auth/register", json=user_data)
        
        # Get user from database
        result = await db_session.execute(
            select(User).where(User.username == user_data["username"])
        )
        user = result.scalar_one()
        
        assert user.is_active is True
        assert user.is_superuser is False

    async def test_email_username_uniqueness_constraint(self, client: AsyncClient):
        """Test database-level uniqueness constraints."""
        user_data = {
            "email": "unique@example.com",
            "username": "uniqueuser",
            "password": "test123"
        }
        
        # First registration should succeed
        response1 = await client.post("/auth/register", json=user_data)
        assert response1.status_code == 200
        data1 = response1.json()
        assert data1["email"] == user_data["email"]
        assert data1["username"] == user_data["username"]
        
        # Second registration with exact same data should fail
        response2 = await client.post("/auth/register", json=user_data)
        assert response2.status_code == 400
        data2 = response2.json()
        assert "Email or username already registered" in data2["detail"]


class TestAuthenticationEdgeCases:
    """Test edge cases and security considerations."""

    async def test_case_sensitive_username_login(self, client: AsyncClient):
        """Test that username login is case-sensitive."""
        user_data = {
            "email": "case@example.com",
            "username": "CaseUser",
            "password": "test123"
        }
        
        await client.post("/auth/register", json=user_data)
        
        # Login with correct case should work
        response1 = await client.post(
            "/auth/login",
            data={"username": "CaseUser", "password": "test123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert response1.status_code == 200
        
        # Login with wrong case should fail
        response2 = await client.post(
            "/auth/login",
            data={"username": "caseuser", "password": "test123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert response2.status_code == 400

    async def test_sql_injection_attempts(self, client: AsyncClient):
        """Test that SQL injection attempts are handled safely."""
        malicious_data = {
            "email": "test'; DROP TABLE users; --@example.com",
            "username": "'; DROP TABLE users; --",
            "password": "test123"
        }
        
        # Should return validation error, not crash
        response = await client.post("/auth/register", json=malicious_data)
        # Should either succeed (if email validation passes) or return 422
        assert response.status_code in [200, 422]

    async def test_long_field_values(self, client: AsyncClient):
        """Test registration with very long field values."""
        long_string = "a" * 1000
        
        long_data = {
            "email": f"{long_string}@example.com",
            "username": long_string,
            "password": long_string
        }
        
        response = await client.post("/auth/register", json=long_data)
        # Should handle gracefully (either succeed or return validation error)
        assert response.status_code in [200, 400, 422]

    async def test_special_characters_in_fields(self, client: AsyncClient):
        """Test registration with special characters."""
        special_data = {
            "email": "test+tag@example.com",
            "username": "user_with-special.chars123",
            "password": "p@$$w0rd!#$"
        }
        
        response = await client.post("/auth/register", json=special_data)
        assert response.status_code in [200, 400, 422]
        
        if response.status_code == 200:
            # If registration succeeds, login should also work
            login_response = await client.post(
                "/auth/login",
                data={"username": special_data["username"], "password": special_data["password"]},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            assert login_response.status_code == 200

    async def test_unicode_characters(self, client: AsyncClient):
        """Test registration with unicode characters."""
        unicode_data = {
            "email": "test@例え.テスト",  # Japanese characters
            "username": "用户名",  # Chinese characters
            "password": "пароль123"  # Cyrillic characters
        }
        
        response = await client.post("/auth/register", json=unicode_data)
        # Should handle gracefully
        assert response.status_code in [200, 400, 422]