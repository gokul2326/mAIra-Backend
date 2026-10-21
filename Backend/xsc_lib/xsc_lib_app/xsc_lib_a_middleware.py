import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from xsc_lib.xsc_lib_app.xsc_lib_a_logging import logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        logger.info(f"{request.method} {request.url.path} -> Status {response.status_code} ({duration_ms:.2f}ms)")
        return response
