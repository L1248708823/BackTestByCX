"""Application entrypoint.

This module creates the FastAPI app instance and wires shared middleware
and API routers. It is imported by the ASGI server process.
"""

from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.schemas.common import ErrorResponse

settings = get_settings()


def create_application() -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        None.

    Returns:
        FastAPI: Configured FastAPI app instance.
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url=f"{settings.api_v1_prefix}/docs",
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """Return the unified validation error payload.

        Args:
            request: Incoming request object.
            exc: Validation exception raised by FastAPI.

        Returns:
            JSONResponse: Unified validation error response.
        """
        error = ErrorResponse(
            code="validation_error",
            message="Request payload validation failed",
            details={
                "path": request.url.path,
                "errors": jsonable_encoder(exc.errors()),
            },
            request_id=f"req_{uuid4().hex[:12]}",
        )
        return JSONResponse(status_code=422, content=error.model_dump(mode="json"))

    @app.exception_handler(HTTPException)
    async def handle_http_exception(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        """Return the unified HTTP error payload.

        Args:
            request: Incoming request object.
            exc: HTTP exception raised by route handlers.

        Returns:
            JSONResponse: Unified HTTP error response.
        """
        error = ErrorResponse(
            code="http_error",
            message=str(exc.detail),
            details={"path": request.url.path},
            request_id=f"req_{uuid4().hex[:12]}",
        )
        return JSONResponse(status_code=exc.status_code, content=error.model_dump(mode="json"))

    @app.get("/", tags=["root"])
    def read_root() -> dict[str, str]:
        """Return a simple root payload.

        Args:
            None.

        Returns:
            dict[str, str]: Service identity payload.
        """
        return {"service": settings.app_name, "version": settings.app_version}

    return app


app = create_application()
