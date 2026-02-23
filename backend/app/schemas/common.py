"""Common API schema models.

This module provides shared response objects reused by multiple endpoints.
"""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Service health payload returned by liveness endpoints.

    Attributes:
        status: Machine-readable health state.
        service: Service identifier for diagnostics.
    """

    status: str = Field(description="Service health state, expected value is 'ok'")
    service: str = Field(description="Service name returned by health endpoint")
