"""
Pydantic request models for Password endpoints.

These models capture the single `password` form-field used by both
`/password/lock` and `/password/unlock` routes.  They include an
`as_form` class-method so they can be supplied to FastAPI's `Depends`
while the endpoint remains `multipart/form-data` (required because the
same request also sends a file upload).
"""

from pydantic import BaseModel, Field

# ? Password APIs


class PasswordAdditionRequest(BaseModel):
    password: str = Field(..., min_length=4, description="Password for the PDF file")


class PasswordRemovalRequest(BaseModel):
    password: str = Field(..., min_length=4, description="Password for the PDF file")
