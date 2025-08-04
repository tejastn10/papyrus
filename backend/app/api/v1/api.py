from fastapi import APIRouter

from app.api.v1.endpoints.password import password
from app.utils.logger import log_info, log_error

api_router: APIRouter = APIRouter()

try:
    api_router.include_router(
        password.router,
        prefix="/password",
        tags=["Password"],
    )

    log_info("API v1 routes configured successfully")

except Exception as e:
    log_error("Failed to configure API routes", error=str(e), exc_info=True)
    raise
