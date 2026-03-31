"""DCA 策略执行实现。

本文件用于承载当前 DCA 单策略的最小执行逻辑。
现阶段先返回确定性的占位结果，用于把策略执行边界从 service 中拆出来。
"""

from __future__ import annotations

from uuid import uuid4

from app.domain.models.market_bar import MarketBar
from app.domain.strategies.base import StrategyBase
from app.infra.data_sources.base import MarketDataProvider
from app.schemas.backtest import (
    BacktestCapitalPoint,
    BacktestDailyRecord,
    BacktestSummary,
    BacktestTimeSeriesPoint,
    DcaBacktestRunRequest,
    DcaBacktestRunResponse,
)


class DcaStrategy(StrategyBase[DcaBacktestRunRequest, DcaBacktestRunResponse]):
    """DCA 策略执行器。"""

    strategy_id = "dca"

    def __init__(self, provider: MarketDataProvider) -> None:
        """初始化 DCA 策略执行器。

        Args:
            provider: 当前回测使用的行情数据源。
        """
        self._provider = provider

    def run(self, payload: DcaBacktestRunRequest) -> DcaBacktestRunResponse:
        """执行一次 DCA 回测并返回结果。

        Args:
            payload: 已通过 Pydantic 校验的 DCA 回测请求体。

        Returns:
            DcaBacktestRunResponse: DCA 回测响应结构。
        """
        bars = self._provider.fetch_bars(
            symbol=payload.symbol,
            start_date=payload.start_date,
            end_date=payload.end_date,
        )
        request_id = f"req_{uuid4().hex[:12]}"
        start_bar = bars[0]
        end_bar = bars[-1]

        summary = BacktestSummary(
            total_return_pct=6.5,
            annualized_return_pct=4.1,
            max_drawdown_pct=-8.2,
            annualized_volatility_pct=11.3,
            sharpe_ratio=0.58,
            trading_days=len(bars),
        )
        nav_series = [
            BacktestTimeSeriesPoint(date=start_bar.trade_date, value=1.0),
            BacktestTimeSeriesPoint(date=end_bar.trade_date, value=1.065),
        ]
        drawdown_series = [
            BacktestTimeSeriesPoint(date=start_bar.trade_date, value=0.0),
            BacktestTimeSeriesPoint(date=end_bar.trade_date, value=-8.2),
        ]
        capital_curve = [
            BacktestCapitalPoint(
                date=start_bar.trade_date,
                invested_capital=payload.initial_capital,
                total_value=payload.initial_capital,
            ),
            BacktestCapitalPoint(
                date=end_bar.trade_date,
                invested_capital=payload.initial_capital + payload.periodic_investment_amount,
                total_value=payload.initial_capital + payload.periodic_investment_amount * 1.065,
            ),
        ]
        records = [
            BacktestDailyRecord(
                date=start_bar.trade_date,
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
                date=end_bar.trade_date,
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

        return DcaBacktestRunResponse(
            run_id=f"run_{uuid4().hex[:12]}",
            request_id=request_id,
            strategy_id=self.strategy_id,
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
