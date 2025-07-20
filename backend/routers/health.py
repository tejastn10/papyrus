from fastapi import APIRouter
from pydantic import BaseModel


class HealthStatus(BaseModel):
    status: str


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "/",
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
