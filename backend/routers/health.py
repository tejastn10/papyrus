from fastapi import APIRouter

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
    responses={
        200: {"description": "Successful health check"},
        404: {"description": "Not found"},
    },
)
async def health():
    return {"status": "healthy"}
