"""DCA 回测 Service。

本文件用于承载 DCA 策略的回测用例编排逻辑。
当前只负责委托具体策略执行，不再内置策略结果构造细节。
"""

from __future__ import annotations

from app.domain.strategies.base import StrategyBase
from app.schemas.backtest import DcaBacktestRunRequest, DcaBacktestRunResponse


class DcaBacktestService:
    """DCA 回测用例 Service。"""

    def __init__(
        self,
        strategy: StrategyBase[DcaBacktestRunRequest, DcaBacktestRunResponse],
    ) -> None:
        """初始化 DCA 回测 Service。

        Args:
            strategy: 当前 DCA 回测要使用的策略执行器。
        """
        self._strategy = strategy

    def run_backtest(self, payload: DcaBacktestRunRequest) -> DcaBacktestRunResponse:
        """执行一次 DCA 回测并返回结果。

        Args:
            payload: 已通过 Pydantic 校验的 DCA 回测请求体。

        Returns:
            DcaBacktestRunResponse: DCA 回测响应结构。
        """
        return self._strategy.run(payload)
