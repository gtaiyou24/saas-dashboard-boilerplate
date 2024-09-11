from typing import override

from fastapi import APIRouter

from common.core import AppModule


class Authority(AppModule):
    @override
    def startup(self) -> None:
        pass

    @override
    def shutdown(self) -> None:
        pass

    @override
    @property
    def router(self) -> APIRouter:
        router = APIRouter(tags=["Authority"])
        return router
