"""标准化行情 K 线模型。

本文件用于定义策略层消费的统一行情结构，屏蔽具体数据源返回格式差异。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class MarketBar:
    """标准化行情 K 线。"""

    trade_date: date
    open: float
    high: float
    low: float
    close: float
    volume: float
    amount: float
    source: str
    adjust_type: str
