from typing import Optional, Generic, TypeVar

from pydantic import BaseModel, Field

# ? Type for generic response wrapper
T = TypeVar("T")


class Meta(BaseModel):
    message: Optional[str] = Field(None, example="Operation successful")
    error_code: Optional[str] = Field(None, example="EMPTY_FILE")
    request_id: Optional[str] = Field(None, example="abc123xyz")


class APIResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    meta: Meta


# * Success responses for each domain


class HealthResponse(BaseModel):
    status: str = Field(..., example="healthy")


class PasswordRemovalResponse(BaseModel):
    message: str = Field(..., example="Password removed successfully")
    filename: str = Field(..., example="document.pdf")
    file_data: str = Field(..., description="Base64-encoded PDF", example="JVBERi0xLjQKJ...")


class PasswordAdditionResponse(BaseModel):
    message: str = Field(..., example="Password added successfully")
    filename: str = Field(..., example="secured.pdf")
    file_data: str = Field(..., description="Base64-encoded PDF", example="JVBERi0xLjQKJ...")


# ! Error schema (non-200 response)


class ErrorResponse(BaseModel):
    message: str = Field(..., example="The uploaded file is not a PDF.")
    error: Optional[str] = Field(None, example="Expected .pdf but got .txt")
