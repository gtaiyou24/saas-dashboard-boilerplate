from di import DIContainer
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from apigateway.application.authorization import AuthorizationApplicationService
from apigateway.application.authorization.command import AuthenticateCommand, RevokeCommand
from apigateway.port.adapter.resource.auth.request import OAuth2PasswordRequest
from apigateway.port.adapter.resource.auth.response import TokenJson
from common.port.adapter.resource import APIResource
from common.port.adapter.resource.error import ErrorJson
from dependency import oauth2_scheme


class AuthResource(APIResource):
    router = APIRouter(prefix="/auth")

    def __init__(self):
        self.__authorization_application_service = None
        self.router.add_api_route(
            "/login",
            self.form_login,
            methods=["POST"],
            response_model=TokenJson,
            responses={403: {"model": ErrorJson}, 401: {"model": ErrorJson}},
            name='フォームログイン',
            include_in_schema=False
        )
        self.router.add_api_route(
            "/token",
            self.token,
            methods=["POST"],
            response_model=TokenJson,
            responses={403: {"model": ErrorJson}, 401: {"model": ErrorJson}},
            name='トークンを発行'
        )
        # self.router.add_api_route("/token", self.refresh, methods=["PUT"], response_model=TokenJson, name='トークンを更新')
        self.router.add_api_route("/token", self.revoke, methods=["DELETE"], name='トークンを削除')

    @property
    def authorization_application_service(self) -> AuthorizationApplicationService:
        self.__authorization_application_service = (
            self.__authorization_application_service or DIContainer.instance().resolve(AuthorizationApplicationService)
        )
        return self.__authorization_application_service

    def form_login(self, form: OAuth2PasswordRequestForm = Depends()) -> TokenJson:
        command = AuthenticateCommand(form.username, form.password)
        dpo = self.authorization_application_service.authenticate(command)
        return TokenJson.from_(dpo)

    def token(self, request: OAuth2PasswordRequest) -> TokenJson:
        """トークンを発行"""
        command = AuthenticateCommand(request.email_address, request.password)
        dpo = self.authorization_application_service.authenticate(command)
        return TokenJson.from_(dpo)

    # def refresh(self, token: str = Depends(oauth2_scheme)) -> TokenJson:
    #     """トークンをリフレッシュ"""
    #     command = RefreshCommand(token)
    #     dpo = self.authorization_application_service.refresh(command)
    #     return TokenJson.from_(dpo)

    def revoke(self, token: str = Depends(oauth2_scheme)) -> None:
        """トークンを削除"""
        command = RevokeCommand(token)
        self.authorization_application_service.revoke(command)
