from typing import override, Literal

from injector import inject

from apigateway.domain.model.user import UserService, EmailAddress, User, UserId
from apigateway.port.adapter.service.user.adapter import UserAdapter


class UserServiceImpl(UserService):
    @inject
    def __init__(self, user_adapter: UserAdapter):
        self.user_adapter = user_adapter

    @override
    def authenticate(self, email_address: EmailAddress, plain_password: str) -> User | None:
        return self.user_adapter.authenticate(email_address, plain_password)

    @override
    def authenticate_with(self, account: Literal["GOOGLE", "GITHUB"], code: str, redirect_uri: str,
                          code_verifier: str) -> User | None:
        return self.user_adapter.authenticate_with(account, code, redirect_uri, code_verifier)

    @override
    def user(self, user_id: UserId) -> User:
        return self.user_adapter.user(user_id)
