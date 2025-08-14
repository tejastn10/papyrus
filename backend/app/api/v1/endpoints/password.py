"""
Password endpoints (API v1)
===========================

Exposes two multipart endpoints under **/password**:

* **POST `/password/lock`**   - Encrypt a PDF with a user-supplied password.
* **POST `/password/unlock`** - Remove an existing password from a PDF.

Both endpoints:

1. Accept a file (`UploadFile`, form-field **file**) and a **password** as form data.
2. Delegate the heavy lifting to `PasswordService.lock` / `PasswordService.unlock`.
3. Return a typed Pydantic response (`PasswordAdditionResponse` or its unlocked sibling) with Base64-encoded PDF bytes.
4. Translate domain-level errors (`FileValidationError`) into `HTTPException` so FastAPI can serialise them and Swagger
can document them.

Error handling
--------------
* **400 Bad Request** - Validation failure (size, MIME type, extension, bad password).
* **418 I'm a teapot** - Catch-all for unexpected processing errors.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.password.main import FileValidationError, PasswordService

from app.models.response import PasswordAdditionResponse, PasswordRemovalResponse

router = APIRouter()


@router.post(
    "/lock",
    response_model=PasswordAdditionResponse,
    summary="Add password to a PDF",
)
async def lock(
    file: UploadFile = File(..., description="PDF file to lock"),
    password: str = Form(..., description="Password for the PDF file"),
):
    """
    Encrypt an uploaded PDF with *password*.

    Parameters
    ----------
    file : UploadFile
        The PDF file to be encrypted.
    password : str
        Password to apply to the PDF.

    Returns
    -------
    PasswordAdditionResponse
        Pydantic model containing the locked PDF (Base64), filename, and message.

    Raises
    ------
    HTTPException
        * 400 - If `FileValidationError` is raised by the service layer.
        * 418 - For any other unexpected failure during processing.
    """
    try:
        return await PasswordService.lock(file, password)
    except FileValidationError as e:
        raise HTTPException(status_code=400, detail={"message": "Bad Request", "error": str(e)}) from e
    except Exception as e:
        raise HTTPException(
            status_code=418,
            detail={"message": "Failed to process PDF", "error": str(e)},
        ) from e


@router.post(
    "/unlock",
    response_model=PasswordRemovalResponse,
    summary="Remove password from a PDF",
)
async def unlock(
    file: UploadFile = File(..., description="PDF file to unlock"),
    password: str = Form(..., description="Password for the PDF file"),
):
    """
    Remove password protection from an uploaded PDF.

    Parameters
    ----------
    file : UploadFile
        The password-protected PDF file.
    password : str
        Password required to unlock the PDF.

    Returns
    -------
    PasswordAdditionResponse
        Pydantic model containing the unlocked PDF (Base64), filename, and message.

    Raises
    ------
    HTTPException
        * 400 - If `FileValidationError` is raised by the service layer.
        * 418 - For any other unexpected failure during processing.
    """
    try:
        return await PasswordService.unlock(file, password)
    except FileValidationError as e:
        raise HTTPException(status_code=400, detail={"message": "Bad Request", "error": str(e)}) from e
    except Exception as e:
        raise HTTPException(
            status_code=418,
            detail={"message": "Failed to process PDF", "error": str(e)},
        ) from e
