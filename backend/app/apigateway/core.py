from typing import override

from di import DIContainer, DI
from fastapi import APIRouter

from apigateway.domain.model.secret import SecretManagerService
from apigateway.domain.model.token import TokenRepository
from apigateway.domain.model.user import UserService
from apigateway.port.adapter.persistence.repository.redis.token import RedisTokenRepository
from apigateway.port.adapter.resource.auth import AuthResource
from apigateway.port.adapter.resource.health import HealthResource
from apigateway.port.adapter.service.secret import SecretManagerServiceImpl
from apigateway.port.adapter.service.secret.adapter import SecretManagerAdapter
from apigateway.port.adapter.service.secret.adapter.stub import SecretManagerAdapterStub
from apigateway.port.adapter.service.user import UserServiceImpl
from apigateway.port.adapter.service.user.adapter import AuthorityAdapter, UserAdapter
from common.core import AppModule


class ApiGateway(AppModule):
    @override
    def startup(self) -> None:
        DIContainer.instance().register(
            # Repository
            DI.of(TokenRepository, {}, RedisTokenRepository),
            # Service
            DI.of(SecretManagerService, {}, SecretManagerServiceImpl),
            DI.of(UserService, {}, UserServiceImpl),
            DI.of(SecretManagerAdapter, {}, SecretManagerAdapterStub),
            DI.of(UserAdapter, {}, AuthorityAdapter)
        )

    @override
    def shutdown(self) -> None:
        pass

    @override
    @property
    def router(self) -> APIRouter:
        router = APIRouter(tags=["API Gateway"])
        router.include_router(AuthResource().router)
        router.include_router(HealthResource().router)
        return router
