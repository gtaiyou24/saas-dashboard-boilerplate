from __future__ import annotations

import abc

from apigateway.domain.model.session import Session, SessionId
from authority.domain.model.user import UserId


class SessionRepository(abc.ABC):
    @abc.abstractmethod
    def next_identity(self) -> SessionId:
        pass

    @abc.abstractmethod
    def save(self, session: Session) -> None:
        pass

    @abc.abstractmethod
    def remove(self, session: Session) -> None:
        pass

    @abc.abstractmethod
    def remove_all(self, *session: Session) -> None:
        pass

    @abc.abstractmethod
    def session_with_token(self, value: str) -> Session | None:
        pass

    @abc.abstractmethod
    def sessions_with_user_id(self, user_id: UserId) -> set[Session]:
        pass

    @abc.abstractmethod
    def get(self, session_id: SessionId) -> Session | None:
        pass
