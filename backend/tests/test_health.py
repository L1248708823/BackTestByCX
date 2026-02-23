"""Health endpoint tests.

This module verifies that the backend application can start and expose
its baseline health-check contract.
"""

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_returns_ok() -> None:
    """Ensure health endpoint returns the expected payload.

    Args:
        None.

    Returns:
        None.
    """
    client = TestClient(app)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "backend"}
