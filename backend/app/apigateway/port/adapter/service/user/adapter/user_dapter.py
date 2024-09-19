import abc

from apigateway.domain.model.user import EmailAddress, User, UserId


class UserAdapter(abc.ABC):
    @abc.abstractmethod
    def authenticate(self, email_address: EmailAddress, plain_password: str) -> User | None:
        pass

    @abc.abstractmethod
    def user(self, user_id: UserId) -> User:
        pass
