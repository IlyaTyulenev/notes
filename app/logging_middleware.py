import json
import logging
import time
from typing import Callable

from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.requests")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        start = time.perf_counter()

        body = b""
        try:
            body = await request.body()
        except Exception:
            pass

        response: Response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000

        user = request.scope.get("user_id", "-")

        logger.info(
            json.dumps(
                {
                    "method": request.method,
                    "path": request.url.path,
                    "status": response.status_code,
                    "user": user,
                    "duration_ms": round(elapsed_ms, 2),
                    "content_length": len(body) if body else 0,
                },
                ensure_ascii=False,
            )
        )
        return response
