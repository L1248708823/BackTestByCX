"""Health-check routes.

This module provides lightweight readiness endpoints for local development
and deployment health probes.
"""

from fastapi import APIRouter

from app.schemas.common import HealthResponse

health_router = APIRouter()


@health_router.get("/health", response_model=HealthResponse)
def get_health_status() -> HealthResponse:
    """Return backend liveness information.

    Args:
        None.

    Returns:
        HealthResponse: Service status payload.
    """
    return HealthResponse(status="ok", service="backend")
