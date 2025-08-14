"""
API v1 router configuration.

This module centralises **all** version-1 endpoint routers into a single
`APIRouter` instance called `api_router`.

Current sub-routers
-------------------
* **Password** - mounted at `/password`, tagged “Password” in Swagger UI.

On import we:

1. Instantiate the parent router (`api_router`).
2. Register each child router with its prefix and tags.
3. Log success or failure via the project-wide logger.

If a router fails to import or register, we log the exception **with
traceback** and then re-raise so the application fails fast during
startup—making bugs obvious.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import password
from app.utils.logger import log_info, log_error

api_v1_router: APIRouter = APIRouter()

try:
    api_v1_router.include_router(
        password.router,
        prefix="/password",
        tags=["Password"],
    )

    log_info("API v1 routes configured successfully")

except Exception as e:
    log_error("Failed to configure API routes", error=str(e), exc_info=True)
    raise
