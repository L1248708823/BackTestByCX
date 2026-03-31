"""策略执行基类。

本文件用于定义策略层的最小公共协议：
- 每个策略都要暴露固定的 `strategy_id`
- 每个策略都要实现 `run`
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class StrategyBase(ABC, Generic[RequestT, ResponseT]):
    """策略执行基类。"""

    strategy_id: str
    engine_version = "backtest-engine.v1"
    metric_definition_version = "metrics.v1"

    @abstractmethod
    def run(self, payload: RequestT) -> ResponseT:
        """执行策略并返回结果。

        Args:
            payload: 已完成边界校验的策略请求体。

        Returns:
            ResponseT: 当前策略约定的执行结果。
        """
