# DCA Route Contract Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the generic single-backtest contract with a DCA-specific route and split request/response schemas into shared base models plus DCA-specific models, without compatibility code.

**Architecture:** Keep one concrete strategy entrypoint at `POST /api/v1/backtests/dca/run`. Model shared request and response fields in base schemas, move DCA-only inputs into `DcaBacktestRunRequest`, and move `input_snapshot` into `DcaBacktestRunResponse` so the response base stays strategy-agnostic. Keep the runtime implementation intentionally minimal: one DCA route, one DCA service, one generated OpenAPI-to-TypeScript output.

**Tech Stack:** FastAPI, Pydantic v2, pytest, React, TypeScript, openapi-typescript

---

### Task 1: Split Backtest Schemas Into Base + DCA Models

**Files:**
- Modify: `backend/app/schemas/backtest.py`
- Test: `backend/tests/test_backtest_schema.py`

- [ ] **Step 1: Write the failing schema test**

Update `backend/tests/test_backtest_schema.py` so it locks the new class names and the `strategy_id` removal from the request model:

```python
"""回测 Schema 导入测试。

本文件用于验证回测 Schema 模块可以正常导入，
并且当前已经导出 DCA 独立路由所需的模型结构。
"""

import importlib
import sys


def test_backtest_schema_module_can_be_imported() -> None:
    """验证回测 Schema 模块可正常导入并导出 DCA 专属模型。"""
    sys.modules.pop("app.schemas.backtest", None)

    module = importlib.import_module("app.schemas.backtest")

    assert hasattr(module, "BacktestRunRequestBase")
    assert hasattr(module, "DcaBacktestRunRequest")
    assert hasattr(module, "BacktestRunResponseBase")
    assert hasattr(module, "DcaBacktestRunResponse")
    assert "strategy_id" not in module.DcaBacktestRunRequest.model_fields
```

- [ ] **Step 2: Run the schema test to verify it fails**

Run:

```bash
cd backend
pytest tests/test_backtest_schema.py -v
```

Expected: FAIL because the new schema classes do not exist yet.

- [ ] **Step 3: Write the minimal schema refactor**

Refactor `backend/app/schemas/backtest.py` so it keeps the existing summary/series/record models, but replaces the generic request/response pair with base + DCA-specific models:

```python
class BacktestRunRequestBase(BaseModel):
    """单次回测公共请求体。"""

    symbol: str = Field(description="ETF 代码，例如 510300；当前约定只接受 A 股 ETF 标的代码")
    start_date: DateType = Field(description="回测开始日期，格式为 YYYY-MM-DD；该日期当天纳入回测区间")
    end_date: DateType = Field(description="回测结束日期，格式为 YYYY-MM-DD；该日期当天纳入回测区间")
    initial_capital: float = Field(
        default=0,
        ge=0,
        description="初始现金，单位为人民币元；表示回测开始时账户已有的可用现金",
    )
    cost_model: CostModelConfig = Field(
        default_factory=CostModelConfig,
        description="本次回测使用的成本模型配置；用于控制佣金、滑点等交易成本口径",
    )

    @model_validator(mode="after")
    def validate_date_range(self) -> "BacktestRunRequestBase":
        """校验日期区间。"""
        if self.start_date > self.end_date:
            raise ValueError("start_date 必须早于或等于 end_date")
        return self


class DcaBacktestRunRequest(BacktestRunRequestBase):
    """DCA 单次回测请求体。"""

    periodic_investment_amount: float = Field(
        default=1000,
        ge=0,
        description="每次定投金额，单位为人民币元；按投资频率触发时投入该金额",
    )
    investment_frequency: Literal["weekly", "monthly"] = Field(
        default="monthly",
        description="定投频率；weekly 表示按周定投，monthly 表示按月定投",
    )
    monthly_investment_day: int | None = Field(
        default=1,
        ge=1,
        le=28,
        description="按月定投时使用的每月执行日，仅在 investment_frequency=monthly 时有效，取值范围 1-28",
    )
    weekly_investment_weekday: Literal[1, 2, 3, 4, 5] | None = Field(
        default=None,
        description="按周定投时使用的执行日，仅在 investment_frequency=weekly 时有效；1 表示周一，5 表示周五",
    )

    @model_validator(mode="after")
    def validate_schedule_fields(self) -> "DcaBacktestRunRequest":
        """校验 DCA 调度字段。"""
        if self.investment_frequency == "monthly":
            if self.monthly_investment_day is None:
                raise ValueError("investment_frequency=monthly 时必须提供 monthly_investment_day")
            if self.weekly_investment_weekday is not None:
                raise ValueError("investment_frequency=monthly 时不能提供 weekly_investment_weekday")

        if self.investment_frequency == "weekly":
            if self.weekly_investment_weekday is None:
                raise ValueError("investment_frequency=weekly 时必须提供 weekly_investment_weekday")
            if self.monthly_investment_day is not None:
                raise ValueError("investment_frequency=weekly 时不能提供 monthly_investment_day")

        return self


class BacktestRunResponseBase(BaseModel):
    """单次回测成功响应公共外壳。"""

    run_id: str = Field(description="本次回测运行 ID；用于标识一次独立运行结果")
    request_id: str = Field(description="本次请求的追踪 ID；用于排查问题和关联日志")
    strategy_id: str = Field(description="本次运行实际执行的策略标识；当前通常为 dca")
    engine_version: str = Field(description="回测引擎版本；用于标记当前结果对应的引擎口径")
    metric_definition_version: str = Field(
        description="指标定义版本；用于标记收益率、回撤、夏普等指标的计算口径版本",
    )
    summary: BacktestSummary = Field(description="结果摘要指标；供结果页指标卡直接展示")
    nav_series: list[BacktestTimeSeriesPoint] = Field(description="净值曲线数据；供结果页净值图直接使用")
    drawdown_series: list[BacktestTimeSeriesPoint] = Field(description="回撤曲线数据；供结果页回撤图直接使用")
    capital_curve: list[BacktestCapitalPoint] = Field(
        description="累计投入与总资产对比曲线；供结果页资金曲线图直接使用",
    )
    records: list[BacktestDailyRecord] = Field(
        description="日级明细记录；供结果页明细表和后续导出能力直接使用",
    )
    message: str = Field(description="执行结果说明；用于告诉前端当前返回的是正式结果还是占位结果")


class DcaBacktestRunResponse(BacktestRunResponseBase):
    """DCA 单次回测成功响应体。"""

    input_snapshot: DcaBacktestRunRequest = Field(
        description="本次运行的 DCA 输入快照；用于可复现性、导出和结果追溯",
    )
```

- [ ] **Step 4: Run the schema test to verify it passes**

Run:

```bash
cd backend
pytest tests/test_backtest_schema.py -v
```

Expected: PASS with the new schema exports.

- [ ] **Step 5: Commit**

```bash
git add backend/app/schemas/backtest.py backend/tests/test_backtest_schema.py
git commit -m "refactor: split dca backtest schemas"
```

### Task 2: Replace Generic Route/Service With DCA-Specific Entry

**Files:**
- Create: `backend/app/api/v1/dca_backtest.py`
- Create: `backend/app/services/dca_backtest_service.py`
- Modify: `backend/app/api/deps.py`
- Modify: `backend/app/api/v1/router.py`
- Modify: `backend/tests/test_backtest.py`
- Remove: `backend/app/api/v1/backtest.py`
- Remove: `backend/app/services/backtest_service.py`

- [ ] **Step 1: Write the failing endpoint tests**

Replace the generic endpoint tests in `backend/tests/test_backtest.py` with DCA-specific expectations:

```python
from fastapi.testclient import TestClient

from app.main import app


def test_dca_backtest_endpoint_returns_frozen_contract_shape() -> None:
    """确保 DCA 回测接口返回约定好的成功结构。"""
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
    assert payload["input_snapshot"]["periodic_investment_amount"] == 1000
    assert "strategy_id" not in payload["input_snapshot"]


def test_old_generic_backtest_route_is_removed() -> None:
    """确保旧的通用回测入口已经删除。"""
    client = TestClient(app)

    response = client.post("/api/v1/backtests/run", json={})

    assert response.status_code == 404


def test_dca_backtest_endpoint_returns_unified_validation_error_shape() -> None:
    """确保 DCA 接口无效请求仍返回统一错误结构。"""
    client = TestClient(app)

    response = client.post(
        "/api/v1/backtests/dca/run",
        json={
            "symbol": "510300",
            "start_date": "2024-12-31",
            "end_date": "2024-01-01",
            "initial_capital": 0,
            "periodic_investment_amount": 1000,
            "investment_frequency": "weekly",
            "monthly_investment_day": 1,
        },
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "validation_error"
    assert payload["message"] == "Request payload validation failed"
    assert payload["request_id"].startswith("req_")
```

- [ ] **Step 2: Run the endpoint tests to verify they fail**

Run:

```bash
cd backend
pytest tests/test_backtest.py -v
```

Expected: FAIL because the new DCA route and DCA-specific service do not exist yet.

- [ ] **Step 3: Write the minimal DCA route and service implementation**

Create `backend/app/services/dca_backtest_service.py` with the current placeholder behavior, but make the strategy explicit in the service instead of reading it from the request:

```python
"""DCA 单次回测服务。

本文件用于承接 DCA 策略的单次回测执行流程。
当前实现仍是稳定占位结果，后续真实 DCA 引擎会直接替换这里的计算逻辑。
"""

from datetime import date
from uuid import uuid4

from app.schemas.backtest import (
    BacktestCapitalPoint,
    BacktestDailyRecord,
    BacktestSummary,
    BacktestTimeSeriesPoint,
    DcaBacktestRunRequest,
    DcaBacktestRunResponse,
)


class DcaBacktestService:
    """DCA 单次回测服务。"""

    engine_version = "backtest-engine.v1"
    metric_definition_version = "metrics.v1"
    strategy_id = "dca"

    def run_backtest(self, payload: DcaBacktestRunRequest) -> DcaBacktestRunResponse:
        """执行一次 DCA 回测占位逻辑。"""
        trading_days = self._calculate_trading_days(payload.start_date, payload.end_date)
        request_id = f"req_{uuid4().hex[:12]}"

        summary = BacktestSummary(
            total_return_pct=6.5,
            annualized_return_pct=4.1,
            max_drawdown_pct=-8.2,
            annualized_volatility_pct=11.3,
            sharpe_ratio=0.58,
            trading_days=trading_days,
        )

        return DcaBacktestRunResponse(
            run_id=f"run_{uuid4().hex[:12]}",
            request_id=request_id,
            strategy_id=self.strategy_id,
            engine_version=self.engine_version,
            metric_definition_version=self.metric_definition_version,
            input_snapshot=payload.model_copy(deep=True),
            summary=summary,
            nav_series=[
                BacktestTimeSeriesPoint(date=payload.start_date, value=1.0),
                BacktestTimeSeriesPoint(date=payload.end_date, value=1.065),
            ],
            drawdown_series=[
                BacktestTimeSeriesPoint(date=payload.start_date, value=0.0),
                BacktestTimeSeriesPoint(date=payload.end_date, value=-8.2),
            ],
            capital_curve=[
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
            ],
            records=[
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
            ],
            message="Backtest skeleton is running; strategy engine will replace placeholder logic.",
        )

    def _calculate_trading_days(self, start_date: date, end_date: date) -> int:
        """计算包含首尾日期的天数。"""
        return max((end_date - start_date).days + 1, 1)
```

Create `backend/app/api/v1/dca_backtest.py`:

```python
"""DCA 回测路由。

本文件用于暴露 DCA 策略的单次回测 HTTP 接口。
路由层只接收请求并委托给 DCA service，不承载业务计算逻辑。
"""

from fastapi import APIRouter, Depends

from app.api.deps import get_dca_backtest_service
from app.schemas.backtest import DcaBacktestRunRequest, DcaBacktestRunResponse
from app.schemas.common import ErrorResponse
from app.services.dca_backtest_service import DcaBacktestService

dca_backtest_router = APIRouter(prefix="/backtests/dca")


@dca_backtest_router.post(
    "/run",
    response_model=DcaBacktestRunResponse,
    responses={
        422: {
            "model": ErrorResponse,
            "description": "Request payload validation failed",
        },
    },
)
def run_dca_backtest(
    payload: DcaBacktestRunRequest,
    service: DcaBacktestService = Depends(get_dca_backtest_service),
) -> DcaBacktestRunResponse:
    """执行一次 DCA 单次回测。"""
    return service.run_backtest(payload)
```

Update `backend/app/api/deps.py` and `backend/app/api/v1/router.py`:

```python
from app.services.dca_backtest_service import DcaBacktestService


def get_dca_backtest_service() -> DcaBacktestService:
    """提供 DCA 单次回测服务实例。"""
    return DcaBacktestService()
```

```python
from app.api.v1.dca_backtest import dca_backtest_router
from app.api.v1.health import health_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router, tags=["health"])
api_v1_router.include_router(dca_backtest_router, tags=["backtest"])
```

Delete the obsolete generic files so the old route and service cannot survive by accident:

```bash
rm backend/app/api/v1/backtest.py
rm backend/app/services/backtest_service.py
```

- [ ] **Step 4: Run the backend tests to verify they pass**

Run:

```bash
cd backend
pytest tests/test_backtest.py tests/test_backtest_schema.py tests/test_health.py -v
```

Expected: PASS with the new DCA route and without the removed generic route.

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/deps.py backend/app/api/v1/router.py backend/app/api/v1/dca_backtest.py backend/app/services/dca_backtest_service.py backend/app/schemas/backtest.py backend/tests/test_backtest.py backend/tests/test_backtest_schema.py
git rm backend/app/api/v1/backtest.py backend/app/services/backtest_service.py
git commit -m "refactor: move backtest endpoint to dca route"
```

### Task 3: Regenerate OpenAPI Types For The Frontend

**Files:**
- Modify: `frontend/src/types/api-schema.ts` (generated)

- [ ] **Step 1: Start the backend with the new route**

Run:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected: the docs page at `http://localhost:8000/api/v1/docs` exposes `POST /api/v1/backtests/dca/run` and no longer exposes `POST /api/v1/backtests/run`.

- [ ] **Step 2: Regenerate the frontend API types**

Run:

```bash
cd frontend
pnpm generate:api-types
```

Expected: `frontend/src/types/api-schema.ts` is regenerated from the latest FastAPI OpenAPI document.

- [ ] **Step 3: Verify the generated file contains the DCA route contract**

Run:

```bash
cd frontend
rg -n '"/api/v1/backtests/dca/run"|DcaBacktestRunRequest|DcaBacktestRunResponse' src/types/api-schema.ts
```

Expected: matches for the new route and the new DCA schema names.

- [ ] **Step 4: Run frontend type checking**

Run:

```bash
pnpm --filter frontend exec tsc -b
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/types/api-schema.ts
git commit -m "chore: regenerate dca api types"
```

### Task 4: Update Runtime Docs And Local TODO

**Files:**
- Modify: `backend/README.md`
- Modify: `docs/startup-runbook.md`
- Modify: `docs/architecture-blueprint.md`
- Modify: `localDoc/TODO.md`

- [ ] **Step 1: Verify which operational docs still mention the removed generic route**

Run:

```bash
rg -n "/api/v1/backtests/run|/api/backtests/run" backend/README.md docs/startup-runbook.md docs/architecture-blueprint.md
```

Expected: matches in the current files before the doc update.

- [ ] **Step 2: Update the operational docs to the DCA route**

Apply these concrete edits:

```md
4. 回测占位接口：`POST /api/v1/backtests/dca/run`
```

```md
2. 单次回测接口 `/api/v1/backtests/dca/run` 返回结构化结果（当前为骨架占位实现）。
```

```md
1. 前端提交参数至 `/api/v1/backtests/dca/run`。
```

Also update any service/file references in `backend/README.md` so they point at `app/api/v1/dca_backtest.py` and `app/services/dca_backtest_service.py`.

- [ ] **Step 3: Record the completed module in `localDoc/TODO.md`**

Append one new done item and one change-log entry so the local project checkpoint stays current:

```md
- [x] 将单次回测入口切换为 DCA 独立路由，并同步拆分 Base/DCA 契约模型
```

```md
- 2026-03-30 | P1 契约模块 | 将单次回测入口切换为 DCA 独立路由，并拆分 Base/DCA 请求响应模型 | `backend/app/api/v1/dca_backtest.py`、`backend/app/services/dca_backtest_service.py`、`backend/app/schemas/backtest.py`、`backend/tests/test_backtest.py`、`frontend/src/types/api-schema.ts`、`docs/startup-runbook.md`、`backend/README.md`、`docs/architecture-blueprint.md`、`localDoc/TODO.md`
```

- [ ] **Step 4: Re-run the doc grep to ensure live docs no longer advertise the old route**

Run:

```bash
rg -n "/api/v1/backtests/run|/api/backtests/run" backend/README.md docs/startup-runbook.md docs/architecture-blueprint.md
```

Expected: no matches.

- [ ] **Step 5: Commit**

```bash
git add backend/README.md docs/startup-runbook.md docs/architecture-blueprint.md localDoc/TODO.md
git commit -m "docs: update dca backtest route references"
```
