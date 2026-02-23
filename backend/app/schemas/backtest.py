"""Backtest API schema models.

This module defines strongly-typed input and output payloads for the
single-run backtest endpoint.
"""

from datetime import date
from pydantic import BaseModel, Field


class BacktestRunRequest(BaseModel):
    """Request payload for running one backtest job.

    Attributes:
        symbol: ETF symbol, for example 510300.
        start_date: Inclusive backtest start date in YYYY-MM-DD.
        end_date: Inclusive backtest end date in YYYY-MM-DD.
        strategy_name: Strategy identifier registered in backend strategy registry.
        initial_capital: Starting cash amount in CNY.
        periodic_investment: Recurring investment amount per period in CNY.
        investment_day: Day-of-month used for periodic investment.
    """

    symbol: str = Field(description="ETF symbol code")
    start_date: date = Field(description="Backtest start date, format YYYY-MM-DD")
    end_date: date = Field(description="Backtest end date, format YYYY-MM-DD")
    strategy_name: str = Field(default="dca", description="Strategy identifier")
    initial_capital: float = Field(
        default=0,
        ge=0,
        description="Initial available capital in CNY",
    )
    periodic_investment: float = Field(
        default=1000,
        ge=0,
        description="Periodic investment amount in CNY",
    )
    investment_day: int = Field(
        default=1,
        ge=1,
        le=28,
        description="Preferred day of month for periodic investment",
    )


class BacktestSummary(BaseModel):
    """Core summary metrics for a completed backtest.

    Attributes:
        total_return_pct: Total return percentage over the full period.
        annualized_return_pct: Annualized return percentage.
        max_drawdown_pct: Maximum drawdown percentage.
        trading_days: Number of simulated calendar days.
    """

    total_return_pct: float = Field(description="Total return percentage")
    annualized_return_pct: float = Field(description="Annualized return percentage")
    max_drawdown_pct: float = Field(description="Maximum drawdown percentage")
    trading_days: int = Field(description="Number of simulated days")


class BacktestRunResponse(BaseModel):
    """Response payload returned after a backtest run request.

    Attributes:
        run_id: Unique identifier for this backtest run.
        strategy_name: Strategy used by this run.
        summary: Aggregated key metrics for quick frontend rendering.
        message: Human-readable status message.
    """

    run_id: str = Field(description="Unique backtest run identifier")
    strategy_name: str = Field(description="Executed strategy identifier")
    summary: BacktestSummary = Field(description="Aggregated backtest metrics")
    message: str = Field(description="Execution status message")
