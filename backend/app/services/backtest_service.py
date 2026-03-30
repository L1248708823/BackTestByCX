"""Backtest service module.

This service coordinates the backtest use case.
Current implementation is a deterministic placeholder for module bootstrap.
"""

from datetime import date
from uuid import uuid4

from app.schemas.backtest import (
    BacktestCapitalPoint,
    BacktestDailyRecord,
    BacktestRunRequest,
    BacktestRunResponse,
    BacktestSummary,
    BacktestTimeSeriesPoint,
)


class BacktestService:
    """Service object for single backtest execution use case."""

    engine_version = "backtest-engine.v1"
    metric_definition_version = "metrics.v1"

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
        request_id = f"req_{uuid4().hex[:12]}"

        # Deterministic bootstrap metrics keep frontend integration stable.
        summary = BacktestSummary(
            total_return_pct=6.5,
            annualized_return_pct=4.1,
            max_drawdown_pct=-8.2,
            annualized_volatility_pct=11.3,
            sharpe_ratio=0.58,
            trading_days=trading_days,
        )

        nav_series = [
            BacktestTimeSeriesPoint(date=payload.start_date, value=1.0),
            BacktestTimeSeriesPoint(date=payload.end_date, value=1.065),
        ]
        drawdown_series = [
            BacktestTimeSeriesPoint(date=payload.start_date, value=0.0),
            BacktestTimeSeriesPoint(date=payload.end_date, value=-8.2),
        ]
        capital_curve = [
            BacktestCapitalPoint(
                date=payload.start_date,
                invested_capital=payload.initial_capital,
                total_value=payload.initial_capital,
            ),
            BacktestCapitalPoint(
                date=payload.end_date,
                invested_capital=payload.initial_capital + payload.periodic_investment_amount,
                total_value=payload.initial_capital + payload.periodic_investment_amount * 1.065,
            ),
        ]
        records = [
            BacktestDailyRecord(
                date=payload.start_date,
                invested_capital=payload.initial_capital,
                cash_balance=payload.initial_capital,
                position_value=0,
                total_value=payload.initial_capital,
                units_held=0,
                nav=1.0,
                drawdown_pct=0,
                event="run_started",
            ),
            BacktestDailyRecord(
                date=payload.end_date,
                invested_capital=payload.initial_capital + payload.periodic_investment_amount,
                cash_balance=0,
                position_value=payload.initial_capital + payload.periodic_investment_amount * 1.065,
                total_value=payload.initial_capital + payload.periodic_investment_amount * 1.065,
                units_held=100,
                nav=1.065,
                drawdown_pct=-8.2,
                event="run_completed",
            ),
        ]

        return BacktestRunResponse(
            run_id=f"run_{uuid4().hex[:12]}",
            request_id=request_id,
            strategy_id=payload.strategy_id,
            engine_version=self.engine_version,
            metric_definition_version=self.metric_definition_version,
            input_snapshot=payload.model_copy(deep=True),
            summary=summary,
            nav_series=nav_series,
            drawdown_series=drawdown_series,
            capital_curve=capital_curve,
            records=records,
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
