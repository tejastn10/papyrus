import time
import uuid

from fastapi import Request
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import log_info


class RequestLogger:
    """Utility class for logging HTTP Requests"""

    @staticmethod
    def log_request(
        request_id: str, method: str, url: str, client_ip: str, user_agent: str = None
    ):
        """Log incoming request details"""
        log_info(
            f"Request {request_id}: {method} {url} from {client_ip}",
            user_agent=user_agent,
            timestamp=datetime.now().isoformat(),
        )

    @staticmethod
    def log_response(
        request_id: str, statuc_code: int, response_time: float, file_size: int = None
    ):
        """Log outgoing response details"""
        log_info(
            f"Response {request_id}: {statuc_code} in {response_time:.3f}s",
            file_size=file_size,
            timestamp=datetime.now().isoformat(),
        )


class RequestMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses"""

    async def dispatch(self, request: Request, call_next):
        # ? Generate unique Request ID
        request_id = uuid.uuid4()

        # ? Get Client IP
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
            # * Process Request
            response = await call_next(request)

            # ? Track response time
            end_time = time.time() - start_time

            # ? Log the outgoing repsonse
            RequestLogger.log_response(
                request_id=request_id,
                statuc_code=response.status_code,
                response_time=end_time,
            )
            return response
        except Exception:
            # ? Calculate response time for failed request
            response_time = time.time() - start_time
            # ? Log the error response data
            RequestLogger.log_response(
                request_id=request_id,
                statuc_code=418,
                response_time=response_time,
            )

            # ! Raising this for FASTApi to handle it
            raise
