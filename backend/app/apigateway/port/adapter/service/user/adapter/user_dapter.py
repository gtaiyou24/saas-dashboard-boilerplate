import abc
from typing import Literal

from apigateway.domain.model.user import EmailAddress, User, UserId


class UserAdapter(abc.ABC):
    @abc.abstractmethod
    def authenticate(self, email_address: EmailAddress, plain_password: str) -> User | None:
        pass

    @abc.abstractmethod
    def authenticate_with(self, account: Literal["GOOGLE", "GITHUB"], code: str, redirect_uri: str,
                          code_verifier: str) -> User | None:
        pass

    @abc.abstractmethod
    def user(self, user_id: UserId) -> User:
        pass
