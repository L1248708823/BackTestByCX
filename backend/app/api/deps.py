"""API 路由依赖注入提供器。

本文件用于集中定义 FastAPI 的依赖注入构造函数，避免在路由处理函数中直接实例化
Service，从而保持路由层轻量、职责清晰。
"""

from app.domain.strategies.dca_strategy import DcaStrategy
from app.infra.data_sources.placeholder_provider import PlaceholderMarketDataProvider
from app.services.dca_backtest_service import DcaBacktestService


def get_dca_backtest_service() -> DcaBacktestService:
    """提供 DCA 回测 Service 实例。

    Args:
        None.

    Returns:
        DcaBacktestService: DCA 回测用例 Service。
    """
    return DcaBacktestService(
        strategy=DcaStrategy(provider=PlaceholderMarketDataProvider()),
    )
