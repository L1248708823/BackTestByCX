"""DCA 回测接口契约测试。

本文件用于验证 DCA 专属回测接口的最小契约：
- 新接口 `/api/v1/backtests/dca/run` 能稳定返回约定结构
- 旧接口 `/api/v1/backtests/run` 已移除
- 无效请求仍返回统一错误结构
"""

from fastapi.testclient import TestClient

from app.main import app


def test_dca_backtest_endpoint_returns_frozen_contract_shape() -> None:
    """确保 DCA 回测接口返回约定的成功结构。

    Args:
        None.

    Returns:
        None.
    """
    client = TestClient(app)

    response = client.post(
        "/api/v1/backtests/dca/run",
        json={
            "symbol": "510300",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "initial_capital": 0,
            "periodic_investment_amount": 1000,
            "investment_frequency": "monthly",
            "monthly_investment_day": 1,
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
    assert payload["input_snapshot"]["periodic_investment_amount"] == 1000
    assert "strategy_id" not in payload["input_snapshot"]
    assert payload["summary"]["annualized_volatility_pct"] == 11.3
    assert payload["summary"]["sharpe_ratio"] == 0.58
    assert len(payload["nav_series"]) == 2
    assert len(payload["drawdown_series"]) == 2
    assert len(payload["capital_curve"]) == 2
    assert len(payload["records"]) == 2


def test_dca_backtest_endpoint_weekly_happy_path_shape() -> None:
    """确保 weekly 模式可以正常回测，并且 input_snapshot 不包含 monthly 字段。"""
    client = TestClient(app)

    response = client.post(
        "/api/v1/backtests/dca/run",
        json={
            "symbol": "510300",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "initial_capital": 0,
            "periodic_investment_amount": 1000,
            "investment_frequency": "weekly",
            "weekly_investment_weekday": 3,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["input_snapshot"]["investment_frequency"] == "weekly"
    assert payload["input_snapshot"]["weekly_investment_weekday"] == 3
    assert "monthly_investment_day" not in payload["input_snapshot"]


def test_backtest_generic_endpoint_is_removed() -> None:
    """确保旧的通用回测入口已移除（返回 404）。"""
    client = TestClient(app)

    response = client.post(
        "/api/v1/backtests/run",
        json={
            "symbol": "510300",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "initial_capital": 0,
            "periodic_investment_amount": 1000,
            "investment_frequency": "monthly",
            "monthly_investment_day": 1,
        },
    )

    assert response.status_code == 404


def test_dca_backtest_endpoint_returns_unified_validation_error_shape() -> None:
    """确保无效请求仍返回统一错误结构。

    Args:
        None.

    Returns:
        None.
    """
    client = TestClient(app)

    response = client.post(
        "/api/v1/backtests/dca/run",
        json={
            "symbol": "510300",
            "start_date": "2024-12-31",
            "end_date": "2024-01-01",
            "monthly_investment_day": 1,
        },
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "validation_error"
    assert payload["message"] == "Request payload validation failed"
    assert payload["request_id"].startswith("req_")


def test_dca_backtest_endpoint_rejects_monthly_missing_monthly_investment_day() -> None:
    """确保 monthly 模式缺少 monthly_investment_day 时会被拒绝。"""
    client = TestClient(app)

    response = client.post(
        "/api/v1/backtests/dca/run",
        json={
            "symbol": "510300",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "initial_capital": 0,
            "periodic_investment_amount": 1000,
            "investment_frequency": "monthly",
        },
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "validation_error"
    assert payload["request_id"].startswith("req_")


def test_dca_backtest_endpoint_rejects_weekly_missing_weekly_investment_weekday() -> None:
    """确保 weekly 模式缺少 weekly_investment_weekday 时会被拒绝。"""
    client = TestClient(app)

    response = client.post(
        "/api/v1/backtests/dca/run",
        json={
            "symbol": "510300",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "initial_capital": 0,
            "periodic_investment_amount": 1000,
            "investment_frequency": "weekly",
        },
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "validation_error"
    assert payload["request_id"].startswith("req_")


def test_dca_backtest_endpoint_rejects_legacy_strategy_id_field() -> None:
    """确保 DCA 接口显式拒绝旧的 strategy_id 字段。"""
    client = TestClient(app)

    response = client.post(
        "/api/v1/backtests/dca/run",
        json={
            "symbol": "510300",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "strategy_id": "dca",
            "initial_capital": 0,
            "periodic_investment_amount": 1000,
            "investment_frequency": "monthly",
            "monthly_investment_day": 1,
        },
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "validation_error"
    assert payload["request_id"].startswith("req_")
