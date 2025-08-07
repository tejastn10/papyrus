from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.password.main import FileValidationError, PasswordService

from app.models.response import PasswordAdditionResponse


router = APIRouter()


@router.post("/lock", response_model=PasswordAdditionResponse)
async def lock(
    file: UploadFile = File(..., description="PDF file to lock"),
    password: str = Form(..., description="Password to add to the PDF"),
):
    try:
        response = await PasswordService.lock(file, password)

        return response
    except FileValidationError as e:
        raise HTTPException(status_code=400, detail={"message": "Bad Request", "error": str(e)})
    except Exception as e:
        raise HTTPException(
            status_code=418,
            detail={"message": "Failed to process PDF", "error": str(e)},
        )


@router.post("/unlock", response_model=PasswordAdditionResponse)
async def unlock(
    file: UploadFile = File(..., description="PDF file to unlock"),
    password: str = Form(..., description="Password to add to the PDF"),
):
    try:
        response = await PasswordService.unlock(file, password)

        return response
    except FileValidationError as e:
        raise HTTPException(status_code=400, detail={"message": "Bad Request", "error": str(e)})
    except Exception as e:
        raise HTTPException(
            status_code=418,
            detail={"message": "Failed to process PDF", "error": str(e)},
        )
