from injector import singleton, inject

from apigateway.application.authorization.command import AuthenticateCommand, RefreshCommand, RevokeCommand, \
    AuthenticateEmailPasswordCommand, AuthenticateAccountCommand
from apigateway.application.authorization.dpo import TokenDpo, UserDpo, InternalTokenDpo
from apigateway.domain.model.secret import SecretManagerService, Key
from apigateway.domain.model.token import TokenRepository, RefreshToken, BearerToken
from apigateway.domain.model.token.internal import InternalToken
from apigateway.domain.model.user import UserService, EmailAddress, User
from common.application import transactional
from common.exception import SystemException, ErrorCode


@singleton
class AuthorizationApplicationService:
    @inject
    def __init__(self,
                 user_service: UserService,
                 token_repository: TokenRepository,
                 secret_manager_service: SecretManagerService):
        self.user_service = user_service
        self.token_repository = token_repository
        self.secret_manager_service = secret_manager_service

    @transactional
    def authenticate(self, command: AuthenticateCommand) -> TokenDpo:
        """ユーザー認証し、アクセストークン、リフレッシュトークンを発行する"""
        if command.oauth_type == AuthenticateCommand.OAuthType.CREDENTIAL:
            command: AuthenticateEmailPasswordCommand
            email_address = EmailAddress(command.email_address)
            user = self.user_service.authenticate(email_address, command.plain_password)
        else:
            command: AuthenticateAccountCommand
            user = self.user_service.authenticate_with(
                command.oauth_type.name, command.code, command.redirect_uri, command.code_verifier)

        if user is None:
            raise SystemException(ErrorCode.AUTHORIZATION_FAILURE, str(command))

        access_token, refresh_token = user.login()
        self.token_repository.add(access_token)
        self.token_repository.add(refresh_token)

        return TokenDpo(access_token, refresh_token)

    @transactional
    def refresh(self, command: RefreshCommand) -> TokenDpo:
        """リフレッシュトークン指定で新しいアクセストークンとリフレッシュトークンを取得できる"""
        refresh_token: RefreshToken | None = self.token_repository.token_with_value(command.refresh_token)
        if refresh_token is None or refresh_token.type_is('ACCESS') or refresh_token.is_expired():
            raise SystemException(ErrorCode.INVALID_TOKEN, f"リフレッシュトークン {command.refresh_token} は無効です。")

        new_access_token, new_refresh_token = refresh_token.refresh()

        self.token_repository.add(new_access_token)
        self.token_repository.add(new_refresh_token)

        self.token_repository.remove(refresh_token)

        return TokenDpo(new_access_token, new_refresh_token)

    @transactional
    def revoke(self, command: RevokeCommand) -> None:
        """リフレッシュトークンもしくはアクセストークン指定で、トークンを削除できる

        詳細な仕様は、https://tex2e.github.io/rfc-translater/html/rfc7009.html を参照してください。
        """
        token: BearerToken | None = self.token_repository.token_with_value(command.token)
        if token is not None:
            self.token_repository.remove(token)

        other_token: BearerToken | None = self.token_repository.token_with_value(token.pair_token)
        if other_token is not None:
            self.token_repository.remove(other_token)

    def identify(self, access_token: str) -> UserDpo:
        """アクセストークン指定でユーザー情報を取得できる"""
        access_token = self.token_repository.token_with_value(access_token)
        user = User(access_token.user_id)

        return UserDpo(user)

    @transactional
    def publish_internal_token(self, access_token_value: str) -> InternalTokenDpo:
        access_token = self.token_repository.token_with_value(access_token_value)
        if access_token is None:
            raise SystemException(ErrorCode.INVALID_TOKEN, f"アクセストークン {access_token_value} は無効です。")
        if access_token.is_expired():
            self.token_repository.remove(access_token)
            raise SystemException(ErrorCode.INVALID_TOKEN, f"アクセストークン {access_token_value} は無効です。")

        user = self.user_service.user(access_token.user_id)
        private_key = self.secret_manager_service.get(Key.JWT_PRIVATE)
        return InternalTokenDpo(InternalToken.generate(user), private_key)
