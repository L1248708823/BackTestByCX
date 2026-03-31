"""占位行情数据源实现。

本文件用于在 AkShare 尚未接入前提供一个可运行的数据源实现，
让策略层先完成对统一 Provider 协议的依赖。
"""

from __future__ import annotations

from datetime import date, timedelta

from app.domain.models.market_bar import MarketBar
from app.infra.data_sources.base import MarketDataProvider


class PlaceholderMarketDataProvider(MarketDataProvider):
    """当前可运行的占位行情数据源。"""

    def fetch_bars(self, symbol: str, start_date: date, end_date: date) -> list[MarketBar]:
        """返回确定性的占位行情序列。

        Args:
            symbol: 标的代码。
            start_date: 开始日期（含）。
            end_date: 结束日期（含）。

        Returns:
            list[MarketBar]: 用于主线开发阶段的最小标准化行情数据。
        """
        middle_date = start_date + timedelta(days=max((end_date - start_date).days // 2, 1))
        return [
            MarketBar(
                trade_date=start_date,
                open=1.0,
                high=1.02,
                low=0.99,
                close=1.0,
                volume=100_000,
                amount=100_000,
                source="placeholder",
                adjust_type="qfq",
            ),
            MarketBar(
                trade_date=middle_date,
                open=1.0,
                high=1.08,
                low=0.98,
                close=1.05,
                volume=120_000,
                amount=126_000,
                source="placeholder",
                adjust_type="qfq",
            ),
            MarketBar(
                trade_date=end_date,
                open=1.05,
                high=1.12,
                low=1.01,
                close=1.065,
                volume=150_000,
                amount=159_750,
                source="placeholder",
                adjust_type="qfq",
            ),
        ]
