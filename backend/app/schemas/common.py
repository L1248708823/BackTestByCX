"""通用接口 Schema 定义。

本文件用于放置多个接口复用的公共响应结构，
避免不同接口各自维护一套近似错误模型或健康检查模型。
"""

from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """健康检查响应体。"""

    status: str = Field(description="服务健康状态；当前预期固定返回 ok")
    service: str = Field(description="服务标识；用于区分当前返回结果来自哪个后端服务")


class ErrorResponse(BaseModel):
    """统一错误响应体。

    说明：
        所有对前端可见的接口错误，最终都应收敛到这套结构，
        避免不同接口返回不同形状的错误对象。
    """

    code: str = Field(description="稳定的机器可读错误码，例如 validation_error")
    message: str = Field(description="给人看的错误摘要，用于前端提示或日志展示")
    details: Any | None = Field(
        default=None,
        description="结构化错误详情；可用于承载字段级校验信息、请求路径或额外调试信息",
    )
    request_id: str = Field(description="请求追踪 ID；用于关联日志、错误排查和用户反馈")
