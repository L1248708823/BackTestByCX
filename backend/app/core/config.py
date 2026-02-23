"""Application configuration module.

This module centralizes environment-driven settings so routers and services
can read a single strongly-typed settings object.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables.

    Attributes:
        app_name: Human-readable service name used in OpenAPI metadata.
        app_version: Semantic version string for release tracking.
        api_v1_prefix: URL prefix for versioned API routes.
        allow_origins: Browser origins allowed by CORS middleware.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = Field(default="BackTestByCX API", description="FastAPI service name")
    app_version: str = Field(default="0.1.0", description="Current backend version")
    api_v1_prefix: str = Field(default="/api/v1", description="Versioned API prefix")
    allow_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173"],
        description="Allowed CORS origins for browser clients",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings object.

    Args:
        None.

    Returns:
        Settings: Parsed settings from environment and defaults.

    Side Effects:
        Reads environment variables the first time it is called.
    """
    return Settings()
