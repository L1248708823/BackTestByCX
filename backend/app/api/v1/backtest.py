"""Backtest routes.

This module exposes HTTP endpoints for running backtest use cases.
Business logic is delegated to service layer objects.
"""

from fastapi import APIRouter, Depends

from app.api.deps import get_backtest_service
from app.schemas.backtest import BacktestRunRequest, BacktestRunResponse
from app.services.backtest_service import BacktestService

backtest_router = APIRouter(prefix="/backtests")


@backtest_router.post("/run", response_model=BacktestRunResponse)
def run_backtest(
    payload: BacktestRunRequest,
    service: BacktestService = Depends(get_backtest_service),
) -> BacktestRunResponse:
    """Run a single backtest job with validated request payload.

    Args:
        payload: User-requested backtest parameters.
        service: Service layer dependency handling backtest orchestration.

    Returns:
        BacktestRunResponse: Structured summary for frontend display.
    """
    return service.run_backtest(payload)
