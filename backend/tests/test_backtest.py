"""Backtest endpoint contract tests.

This module verifies that the placeholder backtest endpoint already exposes
the frozen MVP contract shape for the frontend and later engine work.
"""

from fastapi.testclient import TestClient

from app.main import app


def test_backtest_endpoint_returns_frozen_contract_shape() -> None:
    """Ensure the backtest endpoint returns the agreed success payload.

    Args:
        None.

    Returns:
        None.
    """
    client = TestClient(app)

    response = client.post(
        "/api/v1/backtests/run",
        json={
            "symbol": "510300",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "strategy_id": "dca",
            "initial_capital": 0,
            "periodic_investment_amount": 1000,
            "investment_frequency": "monthly",
            "monthly_investment_day": 1,
            "weekly_investment_weekday": None,
            "cost_model": {
                "enabled": True,
                "commission_rate": 0.0003,
                "min_commission": 5,
                "slippage_rate": 0,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["strategy_id"] == "dca"
    assert payload["engine_version"] == "backtest-engine.v1"
    assert payload["metric_definition_version"] == "metrics.v1"
    assert payload["input_snapshot"]["symbol"] == "510300"
    assert payload["summary"]["annualized_volatility_pct"] == 11.3
    assert payload["summary"]["sharpe_ratio"] == 0.58
    assert len(payload["nav_series"]) == 2
    assert len(payload["drawdown_series"]) == 2
    assert len(payload["capital_curve"]) == 2
    assert len(payload["records"]) == 2


def test_backtest_endpoint_returns_unified_validation_error_shape() -> None:
    """Ensure invalid requests return the unified error payload.

    Args:
        None.

    Returns:
        None.
    """
    client = TestClient(app)

    response = client.post(
        "/api/v1/backtests/run",
        json={
            "symbol": "510300",
            "start_date": "2024-12-31",
            "end_date": "2024-01-01",
            "investment_frequency": "weekly",
            "monthly_investment_day": 1,
        },
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "validation_error"
    assert payload["message"] == "Request payload validation failed"
    assert payload["request_id"].startswith("req_")
