import abc
from typing import override

from di import DIContainer, DI
from fastapi import APIRouter

from common.application import UnitOfWork
from common.port.adapter.persistence.repository.inmem import InMemUnitOfWork
from common.port.adapter.persistence.repository.mysql import MySQLUnitOfWork


class AppModule(abc.ABC):
    """各モジュールでDI設定やルーティングなどを定義させるためのクラス"""
    @abc.abstractmethod
    def startup(self) -> None:
        """アプリ起動前に実行すべき処理を定義する"""
        pass

    @abc.abstractmethod
    def shutdown(self) -> None:
        """アプリ終了時に実行すべき処理をを定義する"""
        pass

    @property
    @abc.abstractmethod
    def router(self) -> APIRouter:
        """ルーティングを定義"""
        pass


class Common(AppModule):
    @override
    def startup(self) -> None:
        DIContainer.instance().register(
            DI.of(UnitOfWork, {"MySQL": MySQLUnitOfWork}, InMemUnitOfWork)
        )

    @override
    def shutdown(self) -> None:
        pass

    @override
    @property
    def router(self) -> APIRouter:
        raise NotImplementedError("CommonモジュールにはAPI Routerがありません。")
