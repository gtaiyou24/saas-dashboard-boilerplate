from fastapi import APIRouter

from apigateway.port.adapter.resource.health import HealthResource
from common.port.adapter.resource import APIResource


class APIGatewayResource(APIResource):
    def __init__(self):
        self.__router = APIRouter(tags=["API Gateway"])
        self.__router.include_router(HealthResource().router)

    @property
    def router(self) -> APIRouter:
        return self.__router
