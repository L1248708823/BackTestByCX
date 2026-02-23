"""API router aggregation for version v1.

This module composes all feature routers into a single APIRouter object.
"""

from fastapi import APIRouter

from app.api.v1.backtest import backtest_router
from app.api.v1.health import health_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router, tags=["health"])
api_v1_router.include_router(backtest_router, tags=["backtest"])
