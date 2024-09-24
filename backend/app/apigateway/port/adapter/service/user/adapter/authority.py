from typing import override, Literal

from apigateway.domain.model.user import EmailAddress, User, UserId
from apigateway.port.adapter.service.user.adapter import UserAdapter
from authority.port.adapter.resource.user import UserResource
from authority.port.adapter.resource.user.request import OAuth2PasswordRequest, AuthorizationCodeRequest
from common.exception import SystemException


class AuthorityAdapter(UserAdapter):
    def __init__(self):
        self.__user_resource = UserResource()

    @override
    def authenticate(self, email_address: EmailAddress, plain_password: str) -> User | None:
        request = OAuth2PasswordRequest(email_address=email_address.text, password=plain_password)
        try:
            response = self.__user_resource.authenticate(request)
            return User(UserId(response.id))
        except SystemException as e:
            e.logging()
            return None

    @override
    def authenticate_with(self, account: Literal["GOOGLE", "GITHUB"], code: str, redirect_uri: str,
                          code_verifier: str) -> User | None:
        try:
            request = AuthorizationCodeRequest(
                code=code, redirect_uri=redirect_uri, code_verifier=code_verifier, grant_type="authorization_code")
            response = self.__user_resource.authenticate_with_account(request)
            return User(UserId(response.id))
        except SystemException as e:
            e.logging()
            return None

    @override
    def user(self, user_id: UserId) -> User:
        dpo = self.__user_resource.identity_application_service.user(user_id.value)
        return User(id=UserId(dpo.user.id.value))
