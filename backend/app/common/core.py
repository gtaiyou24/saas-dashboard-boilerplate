import abc

from fastapi import APIRouter


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
