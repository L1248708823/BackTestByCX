"""DCA 策略执行测试。

本文件用于锁定最小策略层边界：
- `DcaStrategy.run` 必须直接产出 DCA 回测响应
- `DcaBacktestService` 必须委托策略执行，而不是继续内置占位逻辑
- `DcaStrategy` 必须通过行情 Provider 取标准化 bars，而不是自己伪造行情输入
"""

from datetime import date

from app.schemas.backtest import (
    BacktestSummary,
    DcaBacktestRunResponse,
    DcaMonthlyBacktestRunRequest,
)
from app.services.dca_backtest_service import DcaBacktestService


def test_dca_strategy_run_returns_dca_response() -> None:
    """确保 DCA 策略可以直接执行并返回约定响应结构。"""
    from app.domain.strategies.dca_strategy import DcaStrategy
    from app.domain.models.market_bar import MarketBar
    from app.infra.data_sources.base import MarketDataProvider

    class FakeMarketDataProvider(MarketDataProvider):
        """仅用于验证策略取行情调用链的假数据源。"""

        captured_symbol: str | None = None

        def fetch_bars(self, symbol: str, start_date: date, end_date: date) -> list[MarketBar]:
            self.captured_symbol = symbol
            return [
                MarketBar(
                    trade_date=date(2024, 1, 2),
                    open=1,
                    high=1.1,
                    low=0.9,
                    close=1.05,
                    volume=100,
                    amount=105,
                    source="fake",
                    adjust_type="qfq",
                ),
                MarketBar(
                    trade_date=date(2024, 1, 3),
                    open=1.05,
                    high=1.2,
                    low=1,
                    close=1.1,
                    volume=120,
                    amount=132,
                    source="fake",
                    adjust_type="qfq",
                ),
                MarketBar(
                    trade_date=date(2024, 1, 4),
                    open=1.1,
                    high=1.3,
                    low=1.05,
                    close=1.2,
                    volume=150,
                    amount=180,
                    source="fake",
                    adjust_type="qfq",
                ),
            ]

    provider = FakeMarketDataProvider()
    strategy = DcaStrategy(provider=provider)
    payload = DcaMonthlyBacktestRunRequest(
        symbol="510300",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        initial_capital=0,
        periodic_investment_amount=1000,
        investment_frequency="monthly",
        monthly_investment_day=1,
    )

    response = strategy.run(payload)

    assert response.strategy_id == "dca"
    assert response.engine_version == "backtest-engine.v1"
    assert response.metric_definition_version == "metrics.v1"
    assert provider.captured_symbol == "510300"
    assert response.input_snapshot.investment_frequency == "monthly"
    assert response.input_snapshot.monthly_investment_day == 1
    assert response.summary.trading_days == 3


def test_dca_backtest_service_delegates_to_strategy() -> None:
    """确保 DCA Service 通过策略对象执行，而不是内嵌结果构造逻辑。"""
    from app.domain.strategies.base import StrategyBase

    class FakeStrategy(StrategyBase[DcaMonthlyBacktestRunRequest, DcaBacktestRunResponse]):
        """仅用于验证 service 调用链的假策略。"""

        strategy_id = "dca"
        captured_payload: DcaMonthlyBacktestRunRequest | None = None

        def run(self, payload: DcaMonthlyBacktestRunRequest) -> DcaBacktestRunResponse:
            self.captured_payload = payload
            return DcaBacktestRunResponse(
                run_id="run_fake",
                request_id="req_fake",
                strategy_id="dca",
                engine_version="engine.fake",
                metric_definition_version="metrics.fake",
                input_snapshot=payload,
                summary=BacktestSummary(
                    total_return_pct=1,
                    annualized_return_pct=1,
                    max_drawdown_pct=-1,
                    annualized_volatility_pct=1,
                    sharpe_ratio=1,
                    trading_days=10,
                ),
                nav_series=[],
                drawdown_series=[],
                capital_curve=[],
                records=[],
                message="fake",
            )

    payload = DcaMonthlyBacktestRunRequest(
        symbol="510300",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 10),
        initial_capital=0,
        periodic_investment_amount=1000,
        investment_frequency="monthly",
        monthly_investment_day=1,
    )
    strategy = FakeStrategy()
    service = DcaBacktestService(strategy=strategy)

    response = service.run_backtest(payload)

    assert strategy.captured_payload == payload
    assert response.run_id == "run_fake"
    assert response.engine_version == "engine.fake"
