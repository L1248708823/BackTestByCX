"""Application entrypoint.

This module creates the FastAPI app instance and wires shared middleware
and API routers. It is imported by the ASGI server process.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.core.config import get_settings

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
