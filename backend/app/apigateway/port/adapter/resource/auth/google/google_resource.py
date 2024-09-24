from di import DIContainer
from fastapi import APIRouter, Depends

from apigateway.application.authorization import AuthorizationApplicationService
from apigateway.application.authorization.command import AuthenticateAccountCommand
from apigateway.port.adapter.resource.auth.google.request import AuthorizationCodeForm
from apigateway.port.adapter.resource.auth.response import TokenJson
from common.port.adapter.resource import APIResource


class GoogleResource(APIResource):
    def __init__(self):
        self.__authorization_application_service: AuthorizationApplicationService | None = None
        self.__router = APIRouter(prefix="/oauth2/google")
        self.router.add_api_route("/token", self.token, methods=["POST"], response_model=TokenJson)

    @property
    def authorization_application_service(self) -> AuthorizationApplicationService:
        self.__authorization_application_service = (
            self.__authorization_application_service or DIContainer.instance().resolve(AuthorizationApplicationService)
        )
        return self.__authorization_application_service

    def token(self, form: AuthorizationCodeForm = Depends()) -> TokenJson:
        command = AuthenticateAccountCommand(
            AuthenticateAccountCommand.OAuthType.GOOGLE, form.code, form.redirect_uri, form.code_verifier)
        dpo = self.authorization_application_service.authenticate(command)
        return TokenJson.from_(dpo)

    @property
    def router(self) -> APIRouter:
        return self.__router
