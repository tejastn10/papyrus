from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_v1_router

from app.middleware.request import RequestMiddleware

from app.config.core import settings
from app.config.swagger import openapi_kwargs

from app.models.response import HealthResponse, ErrorResponse

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

# * API Routes
app.include_router(api_v1_router)


@app.get(
    "/",
    tags=["Health"],
    summary="Health check endpoint",
    description="Returns the health status of the API.",
    response_description="The health status",
    operation_id="getHealthStatus",
    response_model=HealthResponse,
    responses={
        200: {"description": "Successful health check"},
        500: {
            "description": "Not found",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "message": "Internal server error",
                        "error": None,
                    },
                },
            },
        },
    },
)
async def health():
    """
    Returns the health status of the API.
    """
    return {"status": "healthy"}
