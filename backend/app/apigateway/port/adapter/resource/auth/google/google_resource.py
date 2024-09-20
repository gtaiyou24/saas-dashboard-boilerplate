from fastapi import APIRouter, Depends

from apigateway.port.adapter.resource.auth.google.request import AuthorizationCodeForm
from apigateway.port.adapter.resource.auth.response import TokenJson
from common.port.adapter.resource import APIResource


class GoogleResource(APIResource):
    def __init__(self):
        self.__router = APIRouter(prefix="/oauth2/google")
        self.router.add_api_route("/token", self.token, methods=["POST"], response_model=TokenJson)

    def token(self, form: AuthorizationCodeForm = Depends()) -> TokenJson:
        pass

    @property
    def router(self) -> APIRouter:
        return self.__router
