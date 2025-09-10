"""Extended health endpoint tests."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_db_endpoint_success():
    """Test database health check with successful connection."""
    response = client.get("/health/db")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert data["database"] == "connected"


def test_health_db_endpoint_failure():
    """Test database health check with connection failure."""
    with patch('app.db.base.get_db') as mock_get_db:
        # Mock database session that raises exception
        async def failing_db():
            raise Exception("Database connection failed")

        mock_get_db.return_value = failing_db()

        response = client.get("/health/db")

        # The endpoint should still return 200 but with unhealthy status
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unhealthy"
        assert "database" in data
        assert data["database"] == "disconnected"


def test_health_endpoint_structure():
    """Test health endpoint response structure."""
    response = client.get("/health/")

    assert response.status_code == 200
    data = response.json()

    # Required fields (based on actual endpoint implementation)
    assert "status" in data
    assert "service" in data

    # Verify data types
    assert isinstance(data["status"], str)
    assert isinstance(data["service"], str)
    assert data["status"] == "healthy"
    assert data["service"] == "AI News Aggregator API"
