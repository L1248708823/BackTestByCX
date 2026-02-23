"""Backtest service module.

This service coordinates the backtest use case.
Current implementation is a deterministic placeholder for module bootstrap.
"""

from datetime import date
from uuid import uuid4

from app.schemas.backtest import BacktestRunRequest, BacktestRunResponse, BacktestSummary


class BacktestService:
    """Service object for single backtest execution use case."""

    def run_backtest(self, payload: BacktestRunRequest) -> BacktestRunResponse:
        """Execute a placeholder backtest and return deterministic metrics.

        Args:
            payload: Backtest input payload validated by Pydantic.

        Returns:
            BacktestRunResponse: Structured run output.

        Notes:
            This placeholder keeps API contracts stable while the real strategy
            engine and data provider modules are implemented in later modules.
        """
        trading_days = self._calculate_trading_days(payload.start_date, payload.end_date)

        # Deterministic bootstrap metrics keep frontend integration stable.
        summary = BacktestSummary(
            total_return_pct=6.5,
            annualized_return_pct=4.1,
            max_drawdown_pct=-8.2,
            trading_days=trading_days,
        )

        return BacktestRunResponse(
            run_id=f"run_{uuid4().hex[:12]}",
            strategy_name=payload.strategy_name,
            summary=summary,
            message="Backtest skeleton is running; strategy engine will replace placeholder logic.",
        )

    def _calculate_trading_days(self, start_date: date, end_date: date) -> int:
        """Calculate inclusive day count for date range inputs.

        Args:
            start_date: Inclusive start date.
            end_date: Inclusive end date.

        Returns:
            int: Inclusive day count, minimum value is 1.
        """
        delta_days = (end_date - start_date).days + 1
        return max(delta_days, 1)
