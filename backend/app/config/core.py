"""
Application configuration module.

Defines a `Settings` object (using Pydantic's `BaseSettings`) that loads
all environment-driven configuration for the Papyrus API, including CORS
origins, metadata, and test mode flag.
"""

from typing import List, Union

from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Central configuration class for Papyrus.

    Environment variables are loaded from `.env` by default.  Any field
    declared here can be overridden via env var of the same name
    (case-sensitive, unless you change `case_sensitive` in `Config`).

    Attributes
    ----------
    API_V1_STR : str
        Root path for version-1 routes.
    PROJECT_NAME : str
        Human-readable service name (used in Swagger UI).
    DESCRIPTION : str
        Short description of the API (Swagger UI, OpenAPI).
    VERSION : str
        SemVer-style application version.
    BACKEND_CORS_ORIGINS : List[AnyHttpUrl]
        Whitelisted origins for CORS requests. Accepts a comma-separated
        string or a JSON-style list in the env file.
    TESTING : bool
        Flag that can be flipped in tests to alter behaviour (e.g. skip
        external integrations).
    """

    # — Service metadata —
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "Papyrus"
    DESCRIPTION: str = "Secure API for removing and adding passwords from and to PDF"
    VERSION: str = "0.0.1"

    # — CORS —
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Accept both a JSON list and a simple comma‑separated string for CORS.

        Example env values
        ------------------
        BACKEND_CORS_ORIGINS='["http://localhost","https://myapp.com"]'
        BACKEND_CORS_ORIGINS=http://localhost,https://myapp.com
        """
        if isinstance(v, str) and not v.startswith("["):
            # Comma‑separated list → Python list
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Testing
    TESTING: bool = False

    class Config:
        """Pydantic Config: `.env` file path and case sensitivity."""

        env_file = ".env"
        case_sensitive = True


# Singleton settings object used throughout the app
settings = Settings()
