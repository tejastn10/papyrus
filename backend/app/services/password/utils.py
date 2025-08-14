"""
PDF utility functions for Papyrus.

Provides:
- File validation (`validate_pdf`)
- Filename helpers (`append_state_suffix`)
- Base64 conversion (`encode_pdf_to_base64`)
- Stubs for lock checks / protect / unprotect (to be implemented)

A custom `FileValidationError` is raised whenever the uploaded file
fails validation, ensuring consistent error payloads across the API.
"""

import io
import base64

from typing import Tuple
from pypdf import PdfReader, PdfWriter
from fastapi import UploadFile, HTTPException

from app.models.response import ErrorResponse


class FileValidationError(HTTPException):
    """
    Raised when an uploaded file does not meet PDF validation criteria.

    Wraps your `ErrorResponse` schema in the `detail` field so FastAPI
    returns a consistent JSON shape.
    """

    def __init__(self, message: str) -> None:
        payload = ErrorResponse(message=message).dict()
        super().__init__(status_code=400, detail=payload)

    # ? For logging/debugging
    def __str__(self) -> str:
        return f"400: {self.detail}"


# * Validation


def validate_pdf(file: UploadFile) -> None:
    """
    Validate that *file* is a PDF, <50MB, and has a `.pdf` extension.

    Parameters
    ----------
    file : UploadFile
        File object received from FastAPI's `File`/`UploadFile`.

    Raises
    ------
    FileValidationError
        If any of the checks (size, MIME type, extension) fail.
    """
    if file.size and file.size > 50 * 1024 * 1024:
        raise FileValidationError("File size exceeds 50MB limit")

    if not file.content_type or file.content_type != "application/pdf":
        raise FileValidationError("Only PDF files are allowed")

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise FileValidationError("File must have .pdf extension")


# * Helpers


def append_state_suffix(file_name: str, state: str, *, separator: str = "_") -> str:
    """
    Insert `<separator><state>` before the file extension.
    """
    if "." in file_name:
        stem, ext = file_name.rsplit(".", maxsplit=1)
        return f"{stem}{separator}{state}.{ext}"
    return f"{file_name}{separator}{state}"


def encode_pdf_to_base64(pdf_bytes: bytes) -> str:
    """
    Convert raw PDF bytes to a Base64-encoded string (UTF-8).

    Returns
    -------
    str
        The Base64 representation, ready for JSON transport.
    """
    return base64.b64encode(pdf_bytes).decode("utf-8")


# ? Main utils


def is_pdf_locked(pdf_bytes: bytes, password: str | None = None) -> Tuple[bool, str]:
    """
    Check whether the PDF is encrypted.

    Parameters
    ----------
    pdf_bytes : bytes
        The raw PDF file in memory.
    password : str | None
        Optional password to test unlocking.

    Returns
    -------
    Tuple[bool, str]
        (is_locked, message) - message is usually 'Unlocked' or an error description.

    Notes
    -----
    Currently unimplemented. Integrate PyPDF2 or pikepdf as needed.
    """
    try:
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_reader = PdfReader(pdf_stream)

        if not pdf_reader.is_encrypted:
            return False, "PDF is already unlocked (NO PASSWORD PROTECTION DETECTED)"

        pdf_reader.decrypt(password)
        return True, "Password Validated Successfully"
    except Exception as e:
        return False, str(e) or "Incorrect password provided"


def protect_pdf(pdf_bytes: bytes, password: str) -> bytes:
    """
    Encrypt a PDF with the given *password*.

    Returns
    -------
    bytes
        The encrypted PDF file.

    Notes
    -----
    Currently unimplemented. Use PyPDF2's `PdfWriter().encrypt()` or pikepdf.
    """
    try:
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_reader = PdfReader(pdf_stream)

        if pdf_reader.is_encrypted:
            raise Exception("PDF is already locked")

        pdf_writer = PdfWriter()

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        # ? Encrypt
        pdf_writer.encrypt(password)

        # ? Write Bytes to Buffer
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)

        return output_stream.getvalue()

    except Exception as e:
        if "PDF is already locked" in str(e):
            raise e
        else:
            raise Exception(f"Failed to add password {str(e)}")


def unprotect_pdf(pdf_bytes: bytes, password: str) -> bytes:
    """
    Decrypt a password-protected PDF.

    Returns
    -------
    bytes
        Decrypted PDF bytes.

    Raises
    ------
    FileValidationError
        If the password is incorrect or the file cannot be unlocked.

    Notes
    -----
    Currently unimplemented. Use PyPDF2's `reader.decrypt(password)` or pikepdf.
    """
    try:
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_reader = PdfReader(pdf_stream)

        if not pdf_reader.is_encrypted:
            return pdf_bytes

        # ? Decrypt
        pdf_reader.decrypt(password)

        pdf_writer = PdfWriter()

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        # ? Write Bytes to Buffer
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)

        return output_stream.getvalue()

    except Exception as e:
        raise Exception(f"Failed to remove password {str(e)}")
