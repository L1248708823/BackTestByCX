"""单次回测接口 Schema 定义。

本文件用于定义 `POST /api/v1/backtests/run` 的请求体和响应体结构，
作为后端接口、OpenAPI 文档和前端类型收敛的唯一事实来源之一。
"""

from datetime import date as DateType
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class CostModelConfig(BaseModel):
    """回测成本模型配置。

    说明：
        该结构表示一次回测运行时使用的成本参数。
        当前先保留最小成本模型字段，后续真实引擎接入时继续沿用这套口径。
    """

    enabled: bool = Field(
        default=True,
        description="是否启用交易成本；为 false 时，本次回测忽略佣金和滑点参数",
    )
    commission_rate: float = Field(
        default=0.0003,
        ge=0,
        description="佣金费率，按成交金额乘以该比例计算；单位为比例值，例如 0.0003 表示万分之三",
    )
    min_commission: float = Field(
        default=5,
        ge=0,
        description="单笔交易最低佣金，单位为人民币元；当按费率计算结果低于该值时，取该最低值",
    )
    slippage_rate: float = Field(
        default=0,
        ge=0,
        description="滑点比例占位字段；当前默认值为 0，真实滑点逻辑接入后按该字段生效",
    )


class BacktestRunRequest(BaseModel):
    """单次回测请求体。

    说明：
        该结构描述用户从参数页提交到后端的一次完整回测配置。
        当前虽然 MVP 只落地 `dca`，但 `strategy_id` 属于已明确的核心扩展点，因此保留。
    """

    symbol: str = Field(description="ETF 代码，例如 510300；当前约定只接受 A 股 ETF 标的代码")
    start_date: DateType = Field(description="回测开始日期，格式为 YYYY-MM-DD；该日期当天纳入回测区间")
    end_date: DateType = Field(description="回测结束日期，格式为 YYYY-MM-DD；该日期当天纳入回测区间")
    strategy_id: str = Field(
        default="dca",
        description="策略标识；当前默认且唯一有效值是 dca，后续新增策略时仍沿用该入口字段",
    )
    initial_capital: float = Field(
        default=0,
        ge=0,
        description="初始现金，单位为人民币元；表示回测开始时账户已有的可用现金",
    )
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
    cost_model: CostModelConfig = Field(
        default_factory=CostModelConfig,
        description="本次回测使用的成本模型配置；用于控制佣金、滑点等交易成本口径",
    )

    @model_validator(mode="after")
    def validate_schedule_fields(self) -> "BacktestRunRequest":
        """校验日期区间和定投调度字段。

        入参：
            无。使用模型实例自身字段完成校验。

        出参：
            BacktestRunRequest：校验通过后的当前实例。
        """
        if self.start_date > self.end_date:
            raise ValueError("start_date 必须早于或等于 end_date")

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


class BacktestSummary(BaseModel):
    """回测结果摘要指标。

    说明：
        该结构用于结果页的指标卡区域，是前端展示核心指标的唯一来源。
    """

    total_return_pct: float = Field(description="累计收益率，单位为百分比，例如 6.5 表示 6.5%")
    annualized_return_pct: float = Field(description="年化收益率，单位为百分比")
    max_drawdown_pct: float = Field(description="最大回撤，单位为百分比；通常为负值")
    annualized_volatility_pct: float = Field(description="年化波动率，单位为百分比")
    sharpe_ratio: float = Field(description="夏普比率；当前按后端统一指标定义口径计算")
    trading_days: int = Field(description="本次回测覆盖的交易日数量")


class BacktestTimeSeriesPoint(BaseModel):
    """前端图表使用的通用时间序列点。"""

    date: DateType = Field(description="该数据点对应的交易日期")
    value: float = Field(description="该日期对应的数值；具体含义取决于所在序列")


class BacktestCapitalPoint(BaseModel):
    """投入金额与总资产对比曲线点。"""

    date: DateType = Field(description="该数据点对应的交易日期")
    invested_capital: float = Field(description="截至该日期累计投入的本金，单位为人民币元")
    total_value: float = Field(description="截至该日期账户总资产，单位为人民币元")


class BacktestDailyRecord(BaseModel):
    """结果页明细表使用的日级记录。"""

    date: DateType = Field(description="该明细记录对应的交易日期")
    invested_capital: float = Field(description="截至该日期累计投入本金，单位为人民币元")
    cash_balance: float = Field(description="截至该日期账户剩余现金，单位为人民币元")
    position_value: float = Field(description="截至该日期持仓市值，单位为人民币元")
    total_value: float = Field(description="截至该日期账户总资产，单位为人民币元")
    units_held: float = Field(description="截至该日期持有的份额数量")
    nav: float = Field(description="标准化后的净值；回测起点通常归一为 1")
    drawdown_pct: float = Field(description="该日期的回撤值，单位为百分比；通常为负值")
    event: str | None = Field(
        default=None,
        description="该日期的事件标记，例如 run_started、run_completed；无事件时为空",
    )


class BacktestRunResponse(BaseModel):
    """单次回测成功响应体。

    说明：
        该结构覆盖结果页指标、图表、明细和可追溯信息，
        前端应直接基于该结构渲染，不再自行重组另一套近似数据结构。
    """

    run_id: str = Field(description="本次回测运行 ID；用于标识一次独立运行结果")
    request_id: str = Field(description="本次请求的追踪 ID；用于排查问题和关联日志")
    strategy_id: str = Field(description="本次运行实际执行的策略标识；当前通常为 dca")
    engine_version: str = Field(description="回测引擎版本；用于标记当前结果对应的引擎口径")
    metric_definition_version: str = Field(
        description="指标定义版本；用于标记收益率、回撤、夏普等指标的计算口径版本",
    )
    input_snapshot: BacktestRunRequest = Field(
        description="本次运行的输入快照；用于可复现性、导出和结果追溯",
    )
    summary: BacktestSummary = Field(description="结果摘要指标；供结果页指标卡直接展示")
    nav_series: list[BacktestTimeSeriesPoint] = Field(
        description="净值曲线数据；供结果页净值图直接使用",
    )
    drawdown_series: list[BacktestTimeSeriesPoint] = Field(
        description="回撤曲线数据；供结果页回撤图直接使用",
    )
    capital_curve: list[BacktestCapitalPoint] = Field(
        description="累计投入与总资产对比曲线；供结果页资金曲线图直接使用",
    )
    records: list[BacktestDailyRecord] = Field(
        description="日级明细记录；供结果页明细表和后续导出能力直接使用",
    )
    message: str = Field(description="执行结果说明；用于告诉前端当前返回的是正式结果还是占位结果")
