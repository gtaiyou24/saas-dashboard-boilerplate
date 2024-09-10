import abc

from fastapi import APIRouter


class APIResource(abc.ABC):
    @property
    @abc.abstractmethod
    def router(self) -> APIRouter:
        pass
