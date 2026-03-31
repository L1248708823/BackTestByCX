"""DCA 回测路由。

本文件用于提供 DCA 策略专属的回测入口：
- 路由前缀：/backtests/dca
- 运行接口：POST /run
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
    """运行一次 DCA 回测并返回结果。

    Args:
        payload: DCA 回测请求体（已校验）。
        service: DCA 回测用例 Service。

    Returns:
        DcaBacktestRunResponse: 回测结果结构。
    """
    return service.run_backtest(payload)

