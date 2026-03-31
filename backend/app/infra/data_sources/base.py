"""行情数据源协议。

本文件用于定义策略层使用的最小行情拉取接口。
当前只保留 DCA 单次回测真正需要的 `fetch_bars`。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from app.domain.models.market_bar import MarketBar


class MarketDataProvider(ABC):
    """行情数据源基类。"""

    @abstractmethod
    def fetch_bars(self, symbol: str, start_date: date, end_date: date) -> list[MarketBar]:
        """拉取标准化行情数据。

        Args:
            symbol: 标的代码。
            start_date: 开始日期（含）。
            end_date: 结束日期（含）。

        Returns:
            list[MarketBar]: 已按交易日升序排列的标准化行情序列。
        """
