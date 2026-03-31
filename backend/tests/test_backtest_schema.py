"""回测 Schema 回归测试。

本文件用于锁定 Task1 要求的模型命名、字段与校验逻辑，防止未来被无意破坏。
"""

from datetime import date
from typing import Annotated, get_args, get_origin

import pytest
import importlib
import sys

from fastapi.testclient import TestClient

from app.main import app
from pydantic import TypeAdapter, ValidationError


def test_backtest_schema_exports_and_structure() -> None:
    """验证新 Request/Response 命名存在，旧结构已删除，且 DCA 请求不含 strategy_id。"""
    sys.modules.pop("app.schemas.backtest", None)
    module = importlib.import_module("app.schemas.backtest")

    assert hasattr(module, "BacktestRunRequestBase")
    assert hasattr(module, "DcaBacktestRunRequest")
    assert hasattr(module, "DcaMonthlyBacktestRunRequest")
    assert hasattr(module, "DcaWeeklyBacktestRunRequest")
    assert hasattr(module, "BacktestRunResponseBase")
    assert hasattr(module, "DcaBacktestRunResponse")
    assert not hasattr(module, "BacktestRunRequest")
    assert not hasattr(module, "BacktestRunResponse")
    assert "strategy_id" not in module.DcaMonthlyBacktestRunRequest.model_fields
    assert "strategy_id" not in module.DcaWeeklyBacktestRunRequest.model_fields

    input_snapshot_field = module.DcaBacktestRunResponse.model_fields["input_snapshot"]
    input_snapshot_annotation = input_snapshot_field.annotation
    if get_origin(input_snapshot_annotation) is Annotated:
        input_snapshot_annotation = get_args(input_snapshot_annotation)[0]
    assert set(get_args(input_snapshot_annotation)) == {
        module.DcaMonthlyBacktestRunRequest,
        module.DcaWeeklyBacktestRunRequest,
    }


def test_backtest_run_request_base_date_validation() -> None:
    """验证日期区间校验在 BacktestRunRequestBase 中会触发。"""
    sys.modules.pop("app.schemas.backtest", None)
    module = importlib.import_module("app.schemas.backtest")

    with pytest.raises(ValueError, match="start_date 必须早于或等于 end_date"):
        module.BacktestRunRequestBase(
            symbol="510300",
            start_date=date(2024, 3, 5),
            end_date=date(2024, 3, 1),
        )


def test_dca_backtest_run_request_schedule_validation() -> None:
    """验证 DCA 请求中 monthly/weekly 调度校验逻辑。"""
    sys.modules.pop("app.schemas.backtest", None)
    module = importlib.import_module("app.schemas.backtest")

    adapter = TypeAdapter(module.DcaBacktestRunRequest)

    with pytest.raises(ValidationError) as monthly_with_weekday:
        adapter.validate_python(
            {
                "symbol": "510300",
                "start_date": date(2024, 1, 1),
                "end_date": date(2024, 12, 31),
                "investment_frequency": "monthly",
                "monthly_investment_day": 1,
                "weekly_investment_weekday": 2,
            }
        )
    assert any(
        "weekly_investment_weekday" in [str(part) for part in err.get("loc", ())]
        for err in monthly_with_weekday.value.errors()
    )

    with pytest.raises(ValidationError) as weekly_with_month_day:
        adapter.validate_python(
            {
                "symbol": "510300",
                "start_date": date(2024, 1, 1),
                "end_date": date(2024, 12, 31),
                "investment_frequency": "weekly",
                "weekly_investment_weekday": 2,
                "monthly_investment_day": 5,
            }
        )
    assert any(
        "monthly_investment_day" in [str(part) for part in err.get("loc", ())]
        for err in weekly_with_month_day.value.errors()
    )


def test_dca_monthly_requires_monthly_investment_day() -> None:
    """验证 monthly 模式必须传入 monthly_investment_day。"""
    sys.modules.pop("app.schemas.backtest", None)
    module = importlib.import_module("app.schemas.backtest")

    adapter = TypeAdapter(module.DcaBacktestRunRequest)
    with pytest.raises(ValidationError) as exc_info:
        adapter.validate_python(
            {
                "symbol": "510300",
                "start_date": date(2024, 1, 1),
                "end_date": date(2024, 12, 31),
                "investment_frequency": "monthly",
            }
        )
    assert any(
        "monthly_investment_day" in [str(part) for part in err.get("loc", ())]
        for err in exc_info.value.errors()
    )


def test_dca_weekly_requires_weekly_investment_weekday() -> None:
    """验证 weekly 模式必须传入 weekly_investment_weekday。"""
    sys.modules.pop("app.schemas.backtest", None)
    module = importlib.import_module("app.schemas.backtest")

    adapter = TypeAdapter(module.DcaBacktestRunRequest)
    with pytest.raises(ValidationError) as exc_info:
        adapter.validate_python(
            {
                "symbol": "510300",
                "start_date": date(2024, 1, 1),
                "end_date": date(2024, 12, 31),
                "investment_frequency": "weekly",
            }
        )
    assert any(
        "weekly_investment_weekday" in [str(part) for part in err.get("loc", ())]
        for err in exc_info.value.errors()
    )


def test_dca_weekly_allows_weekday_only() -> None:
    """验证 weekly 模式只需要 weekly_investment_weekday 即可通过。"""
    sys.modules.pop("app.schemas.backtest", None)
    module = importlib.import_module("app.schemas.backtest")

    adapter = TypeAdapter(module.DcaBacktestRunRequest)
    parsed = adapter.validate_python(
        {
            "symbol": "510300",
            "start_date": date(2024, 1, 1),
            "end_date": date(2024, 12, 31),
            "investment_frequency": "weekly",
            "weekly_investment_weekday": 3,
        }
    )
    assert isinstance(parsed, module.DcaWeeklyBacktestRunRequest)


def test_openapi_dca_run_request_schema_is_discriminated_union() -> None:
    """验证 OpenAPI 能表达 weekly/monthly 两种合法形状，而不是宽松可选对象。"""
    client = TestClient(app)
    openapi = client.get("/api/v1/openapi.json").json()

    request_schema_ref = (
        openapi["paths"]["/api/v1/backtests/dca/run"]["post"]["requestBody"]["content"]["application/json"]["schema"]
    )

    def resolve_ref(schema: dict) -> dict:
        ref = schema.get("$ref")
        if not ref:
            return schema
        assert ref.startswith("#/")
        node: object = openapi
        for part in ref.removeprefix("#/").split("/"):
            assert isinstance(node, dict)
            node = node[part]
        assert isinstance(node, dict)
        return node

    request_schema = resolve_ref(request_schema_ref)
    assert "oneOf" in request_schema
    assert request_schema.get("discriminator", {}).get("propertyName") == "investment_frequency"

    variant_schemas = [resolve_ref(item) for item in request_schema["oneOf"]]
    assert len(variant_schemas) == 2

    def get_frequency_value(schema: dict) -> str:
        frequency_schema = schema["properties"]["investment_frequency"]
        if "const" in frequency_schema:
            return frequency_schema["const"]
        enum = frequency_schema.get("enum")
        assert isinstance(enum, list) and len(enum) == 1
        return enum[0]

    variants_by_frequency = {get_frequency_value(s): s for s in variant_schemas}
    assert set(variants_by_frequency.keys()) == {"monthly", "weekly"}

    assert "monthly_investment_day" in variants_by_frequency["monthly"].get("required", [])
    assert "weekly_investment_weekday" in variants_by_frequency["weekly"].get("required", [])

    assert "weekly_investment_weekday" not in variants_by_frequency["monthly"].get("properties", {})
    assert "monthly_investment_day" not in variants_by_frequency["weekly"].get("properties", {})
