from fastapi import UploadFile

from app.models.response import PasswordRemovalResponse, PasswordAdditionResponse

from app.utils.logger import log_info, log_error

from utils import (
    validate_pdf,
    append_state_suffix,
    encode_pdf_to_base64,
    is_pdf_locked,
    protect_pdf,
    unprotect_pdf,
    FileValidationError,
)


class PasswordService:
    """Service class for PDF Password related operations"""

    @staticmethod
    async def process_password_removal(file: UploadFile, password: str) -> PasswordRemovalResponse:
        """Removes password from the PDF file

        Args:
            file (UploadFile): Uploaded PDF File
            password (str): Password for the PDF

        Returns:
            PasswordRemovalResponse: Unlocked PDF file

        Raises:
            FileValidationError: Validation for file failed
            Exception: If password is incorrect or processing file fails
        """
        try:
            # ? Validate File
            validate_pdf(file=file)

            # ? Read File Content into memory
            pdf_data = await file.read()

            # * Validate Password for PDF
            valid, message = is_pdf_locked(pdf_bytes=pdf_data, password=password)

            if not valid:
                raise Exception(message)

            unlocked_pdf_data = unprotect_pdf(pdf_bytes=pdf_data, password=password)
            encoded_pdf = encode_pdf_to_base64(unlocked_pdf_data)
            filename = append_state_suffix(file.filnename, "unlocked")

            log_info(f"Successfully processed PDF: {file.filename}")

            return PasswordRemovalResponse(
                message="Password removed successfully",
                filename=filename,
                file_data=encoded_pdf,
            )

        except FileValidationError as e:
            log_error(f"File Validation error: {str(e)}")
            raise e
        except Exception as e:
            log_error(f"PDF processing error: {str(e)}")
            raise e
        finally:
            # * Memory cleanup
            if "pdf_data" in locals():
                del pdf_data
            if "unlocked_pdf_data" in locals():
                del unlocked_pdf_data

    @staticmethod
    async def process_password_addition(file: UploadFile, password: str) -> PasswordAdditionResponse:
        """Adds password to the PDF File

        Args:
            file (UploadFile): Uploaded PDF File
            password (str): Password for the PDF

        Returns:
            PasswordAdditionResponse: Locked PDF File

        Raises:
            FileValidationError: Validation for file failed
            Exception: If PDF is already locked or processing file fails
        """
        try:
            # ? Validate File
            validate_pdf(file)

            # ? Read File Content into memory
            pdf_data = await file.read()

            locked_pdf_data = protect_pdf(pdf_bytes=pdf_data, password=password)
            encoded_pdf = encode_pdf_to_base64(locked_pdf_data)
            filename = append_state_suffix(file.filnename, "locked")

            log_info(f"Successfully processed PDF: {file.filename}")

            return PasswordRemovalResponse(
                message="Password added successfully",
                filename=filename,
                file_data=encoded_pdf,
            )

        except FileValidationError as e:
            log_error(f"File Validation error: {str(e)}")
            raise e
        except Exception as e:
            log_error(f"PDF processing error: {str(e)}")
            raise e
        finally:
            # * Memory cleanup
            if "pdf_data" in locals():
                del pdf_data
            if "locked_pdf_data" in locals():
                del locked_pdf_data
