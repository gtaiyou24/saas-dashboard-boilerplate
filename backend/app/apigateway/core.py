from typing import override

from fastapi import APIRouter

from apigateway.port.adapter.resource.health import HealthResource
from common.core import AppModule


class ApiGateway(AppModule):
    @override
    def startup(self) -> None:
        pass

    @override
    def shutdown(self) -> None:
        pass

    @override
    @property
    def router(self) -> APIRouter:
        router = APIRouter(tags=["API Gateway"])
        router.include_router(HealthResource().router)
        return router
