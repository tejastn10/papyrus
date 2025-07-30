from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.request import RequestMiddleware

from app.config.core import settings
from app.config.swagger import openapi_kwargs

from app.models.health import HealthStatus

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    **openapi_kwargs,
)

# * Setting Required Middlewares
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# * Setting Custom Middlewares
app.add_middleware(RequestMiddleware)


@app.get(
    "/",
    tags=["Health"],
    summary="Health check endpoint",
    description="Returns the health status of the API.",
    response_description="The health status",
    operation_id="getHealthStatus",
    response_model=HealthStatus,
    responses={
        200: {"description": "Successful health check"},
        404: {"description": "Not found"},
    },
)
async def health():
    """
    Returns the health status of the API.
    """
    return {"status": "healthy"}
