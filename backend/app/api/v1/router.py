"""v1 API 路由聚合器。

本文件用于聚合并注册 v1 版本下的各业务路由，统一挂载到一个 APIRouter，
由应用入口在 `/api/v1` 前缀下整体引入。
"""

from fastapi import APIRouter

from app.api.v1.dca_backtest import dca_backtest_router
from app.api.v1.health import health_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router, tags=["health"])
api_v1_router.include_router(dca_backtest_router, tags=["backtest"])
