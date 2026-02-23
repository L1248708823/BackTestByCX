"""Dependency providers for API routes.

This module keeps route constructors lightweight by exposing typed dependency
factory functions.
"""

from app.services.backtest_service import BacktestService


def get_backtest_service() -> BacktestService:
    """Provide a backtest service instance for request handlers.

    Args:
        None.

    Returns:
        BacktestService: Service object used by backtest routes.
    """
    return BacktestService()
