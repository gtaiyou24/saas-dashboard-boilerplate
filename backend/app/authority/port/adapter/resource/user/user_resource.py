from di import DIContainer
from fastapi import APIRouter

from authority.application.identity import IdentityApplicationService
from authority.application.identity.command import RegisterUserCommand, ForgotPasswordCommand, ResetPasswordCommand
from authority.port.adapter.resource.user.request import RegisterTenantRequest, ForgotPasswordRequest, \
    ResetPasswordRequest

from common.port.adapter.resource import APIResource


class UserResource(APIResource):
    router = APIRouter(prefix="/users")

    def __init__(self):
        self.__identity_application_service = None
        self.router.add_api_route("/register", self.register, methods=["POST"], name="ユーザー登録")
        self.router.add_api_route("/unregister", self.unregister, methods=["DELETE"], name="ユーザー削除")
        # self.router.add_api_route(
        #     "/verify-email/{token}",
        #     self.verify_email,
        #     methods=["POST"],
        #     response_model=None,
        #     name='メールアドレス検証'
        # )
        # self.router.add_api_route("/forgot-password", self.forgot_password, methods=["POST"], name='パスワードリセット')
        # self.router.add_api_route("/reset-password", self.reset_password, methods=["POST"], name='パスワード再設定')
        # self.router.add_api_route("/change-password", self.change_password, methods=["POST"], name="パスワード更新")

    @property
    def identity_application_service(self) -> IdentityApplicationService:
        self.__identity_application_service = (
            self.__identity_application_service or DIContainer.instance().resolve(IdentityApplicationService)
        )
        return self.__identity_application_service

    def register(self, request: RegisterTenantRequest) -> None:
        """ユーザー登録"""
        command = RegisterUserCommand(
            RegisterUserCommand.Tenant(request.username),
            RegisterUserCommand.User(request.username, request.email_address, request.password)
        )
        self.identity_application_service.register(command)

    def unregister(self) -> None:
        """ユーザー削除"""
        pass

    def verify_email(self, token: str) -> None:
        """メールアドレス検証"""
        self.identity_application_service.verify_email(token)

    def forgot_password(self, request: ForgotPasswordRequest) -> None:
        command = ForgotPasswordCommand(request.email_address)
        self.identity_application_service.forgot_password(command)

    def reset_password(self, request: ResetPasswordRequest) -> None:
        command = ResetPasswordCommand(reset_token=request.token, password=request.password)
        self.identity_application_service.reset_password(command)

    def change_password(self) -> None:
        pass
