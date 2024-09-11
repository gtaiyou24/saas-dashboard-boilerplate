import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class MonitoringMiddleware(BaseHTTPMiddleware):
    """エラー / ログ監視を行うミドルウェア"""
    async def dispatch(self, request: Request, call_next):
        # TODO : Sentry / New Relic へエラー/ログを送信する
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        print(f"##### MonitoringMiddleware: process_time={process_time} #####")
        return response
