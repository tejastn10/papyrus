"""
Request logging middleware and helpers.

Adds a unique request-ID to every incoming request, logs both the
request and the corresponding response (including timing), and
delegates all formatting to `app.utils.logger.log_info`.
"""

import time
import uuid

from fastapi import Request
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import log_info


class RequestLogger:
    """
    Stateless helper for request / response logging.

    The logger writes:
    - Request ID (uuid4)
    - Method + URL
    - Client IP
    - User agent
    - Status code
    - Response time
    - Optional file size (when streaming files)
    """

    @staticmethod
    def log_request(
        *,
        request_id: str,
        method: str,
        url: str,
        client_ip: str,
        user_agent: str | None = None,
    ) -> None:
        """
        Write an INFO-level log line for an incoming request.

        Args:
            request_id: Correlation ID (uuid4).
            method: HTTP method, e.g. GET/POST.
            url: Full URL as received by FastAPI.
            client_ip: Remote client's IP address.
            user_agent: Raw User-Agent header, if present.
        """
        log_info(
            f"Request {request_id}: {method} {url} from {client_ip}",
            user_agent=user_agent,
            timestamp=datetime.now().isoformat(),
        )

    @staticmethod
    def log_response(
        *,
        request_id: str,
        status_code: int,
        response_time: float,
        file_size: int | None = None,
    ) -> None:
        """
        Write an INFO-level log line for the outgoing response.

        Args:
            request_id: Correlation ID used in `log_request`.
            status_code: HTTP status code (e.g. 200, 404).
            response_time: Time taken to serve the request, in seconds.
            file_size: Optional size in bytes for streamed files.
        """
        log_info(
            f"Response {request_id}: {status_code} in {response_time:.3f}s",
            file_size=file_size,
            timestamp=datetime.now().isoformat(),
        )


class RequestMiddleware(BaseHTTPMiddleware):
    """
    ASGI middleware that logs every request/response pair.

    * Generates a UUID-based request ID.
    * Captures client IP and User-Agent.
    * Measures processing time (`call_next`).
    * Logs an error response if an unhandled exception bubbles up.
    """

    async def dispatch(self, request: Request, call_next):
        # ? Generate unique request ID
        request_id = str(uuid.uuid4())

        # ? Determine client IP (may be "UNKNOWN" for some ASGI servers)
        client_ip = request.client.host if request.client else "UNKNOWN"

        # ? Log the incoming request
        RequestLogger.log_request(
            request_id=request_id,
            method=request.method,
            url=str(request.url),
            client_ip=client_ip,
            user_agent=request.headers.get("user-agent"),
        )

        # ? Track start time
        start_time = time.time()

        try:
            # * Hand control to the downstream application
            response = await call_next(request)
            elapsed = time.time() - start_time

            # ? Log success response
            RequestLogger.log_response(
                request_id=request_id,
                status_code=response.status_code,
                response_time=elapsed,
            )
            return response

        except Exception:
            # ? Always log the error case with status 500 (or custom code)
            elapsed = time.time() - start_time
            RequestLogger.log_response(
                request_id=request_id,
                status_code=500,
                response_time=elapsed,
            )
            # ! Re-raise so FastAPI’s global exception handler deals with it
            raise
