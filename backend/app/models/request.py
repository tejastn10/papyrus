from pydantic import BaseModel, Field

# ? Password APIs


class PasswordRemovalRequest(BaseModel):
    password: str = Field(..., min_length=4, description="Password for the PDF file")
