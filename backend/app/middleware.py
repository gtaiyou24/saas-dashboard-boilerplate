import datetime
import time
import uuid

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class MonitoringMiddleware(BaseHTTPMiddleware):
    """エラー / ログ監視を行うミドルウェア"""
    async def dispatch(self, request: Request, call_next):
        # TODO : Sentry / New Relic へエラー/ログを送信する
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        print(f"##### MonitoringMiddleware: process_time={process_time} #####")
        return response


class PublishInternalTokenMiddleware(BaseHTTPMiddleware):
    """アクセストークン、リフレッシュトークンなどの外部通信用トークンをもとに内部通信用トークンを発行するミドルウェア

    内部通信用トークンのペイロードについては、以下の資料を参照してください。
    * https://zenn.dev/mikakane/articles/tutorial_for_jwt
    * https://techblog.yahoo.co.jp/advent-calendar-2017/jwt/
    * https://qiita.com/KWS_0901/items/00446f9df1cdaadf36fc
    """
    http_bearer = HTTPBearer(auto_error=False)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        authorization: HTTPAuthorizationCredentials | None = await self.http_bearer(request)
        if authorization is None:
            return await call_next(request)

        external_token = authorization.credentials
        internal_token_id = uuid.uuid4()
        now = datetime.datetime.now()
        exp = now + datetime.timedelta(seconds=10)
        payload = {
            "iss": "api-gateway",  # JWTの発行者を表す識別子(issuer)。マイクロサービス化した場合は、API Gateway から発行されるため、API Gateway の URLとなる。
            "sub": "internal-token",  # ユーザーの識別子(subject)。通常ユーザーのIDとなる。
            "aud": request.url,  # JWTを利用するクライアント識別子で最初にリクエストを受信するモジュール名ないしはマイクロサービス名(audience)。通常 URI 形式で提供される。
            "iat": int(round(now.timestamp())),  # JWT の発行日時のタイムスタンプ(issued at)
            "nbf": int(round(now.timestamp())),  # JWT が有効となる日時のタイムスタンプ(not before)
            "exp": int(round(exp.timestamp())),  # JWT の有効期限のタイムスタンプ(expiration)
            "jti": internal_token_id,  # JWT の一意な識別子
            "user_id": str(uuid.uuid4()),
            "belong_to": [{"id": "テナント1のID", "projects": ["プロジェクト1"]}, {"id": "テナント2のID", "projects": ["プロジェクト2"]}]
        }
        request.headers.__dict__["_list"].append((b'x-internal-token', b'yyy'))
        response = await call_next(request)
        return response
