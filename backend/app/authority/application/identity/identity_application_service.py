from injector import singleton, inject

from authority.application.identity.command import RegisterUserCommand, ForgotPasswordCommand, ResetPasswordCommand, \
    AuthenticateCommand
from authority.application.identity.dpo import TenantDpo, UserDpo
from authority.application.identity.subscriber import VerificationTokenGeneratedSubscriber, PasswordForgotSubscriber
from authority.domain.model.mail import SendMailService, EmailAddress
from authority.domain.model.tenant import TenantRepository, Tenant
from authority.domain.model.tenant.project import ProjectRepository
from authority.domain.model.user import UserRepository, User, Token
from common.application import transactional
from common.domain.model import DomainEventPublisher
from common.exception import SystemException, ErrorCode


@singleton
class IdentityApplicationService:
    @inject
    def __init__(self,
                 project_repository: ProjectRepository,
                 send_mail_service: SendMailService,
                 tenant_repository: TenantRepository,
                 user_repository: UserRepository):
        self.project_repository = project_repository
        self.send_mail_service = send_mail_service
        self.tenant_repository = tenant_repository
        self.user_repository = user_repository

    @transactional
    def register(self, command: RegisterUserCommand) -> TenantDpo:
        """ユーザー登録

        ユーザーを登録する際に以下の情報も登録する。また、ユーザーが登録されたときに、メアド検証メールを送信する。

        - テナント : 契約単位としての概念。
        - ユーザー : 認証/認可の単位となる概念であり、サービスを利用する実体。登録時にテナントの管理者として、登録する。
        - プロジェクト : テナントはいくつかのプロジェクトを管理することができる。会社の場合は、各部署ごとにプロジェクトを作成し、操作する。
                       テナント登録時は、’No Project’というプロジェクトを登録し、ユーザーはそのプロジェクト以下で操作する。
        """
        # サブスクライバを登録
        DomainEventPublisher.instance().subscribe(VerificationTokenGeneratedSubscriber())

        # テナントを作成
        tenant_id = self.tenant_repository.next_identity()
        tenant = Tenant.provision(tenant_id, command.tenant.name)

        # ユーザーを新規作成
        user_id = self.user_repository.next_identity()
        email_address = EmailAddress(command.user.email_address)
        user = User.provision(user_id, command.user.username, email_address, command.user.plain_password)

        # ユーザーをテナントに管理者として追加
        tenant.register_admin_member(user)
        # プロジェクトを作成
        project_id = self.project_repository.next_identity()
        project = tenant.create_project(project_id, 'Default Project')

        self.user_repository.add(user)
        self.tenant_repository.add(tenant)
        self.project_repository.add(project)
        return TenantDpo(tenant)

    @transactional
    def verify_email(self, verification_token: str) -> None:
        """メアド検証トークン指定でユーザーを有効化し、セッションを発行する"""
        user = self.user_repository.user_with_token(verification_token)
        if user is None or user.token_with(verification_token).has_expired():
            raise SystemException(ErrorCode.VALID_TOKEN_DOES_NOT_EXISTS, f"{verification_token}は無効なトークンです。")

        user.verified()
        self.user_repository.add(user)

    @transactional
    def forgot_password(self, command: ForgotPasswordCommand) -> None:
        # サブスクライバを登録
        DomainEventPublisher.instance().subscribe(PasswordForgotSubscriber())

        email_address = EmailAddress(command.email_address)
        user = self.user_repository.user_with_email_address(email_address)
        if user is None:
            raise SystemException(
                ErrorCode.USER_DOES_NOT_FOUND,
                f"{email_address.text} に紐づくユーザーが見つからなかったため、パスワードリセットメールを送信できませんでした。",
            )

        user.generate(Token.Type.PASSWORD_RESET)
        self.user_repository.add(user)

    @transactional
    def reset_password(self, command: ResetPasswordCommand) -> None:
        """新しく設定したパスワードとパスワードリセットトークン指定で新しいパスワードに変更する"""
        user = self.user_repository.user_with_token(command.reset_token)
        if user is None or user.token_with(command.reset_token).has_expired():
            raise SystemException(
                ErrorCode.VALID_TOKEN_DOES_NOT_EXISTS,
                f"指定したトークン {command.reset_token} は無効なのでパスワードをリセットできません。",
            )

        user.reset_password(command.password, command.reset_token)
        self.user_repository.add(user)

    @transactional
    def authenticate(self, command: AuthenticateCommand) -> UserDpo:
        """ユーザー認証し、セッションを発行する"""
        email_address = EmailAddress(command.email_address)
        user = self.user_repository.user_with_email_address(email_address)

        # 該当ユーザーが存在するか、パスワードは一致しているか
        if user is None or not user.verify_password(command.password):
            raise SystemException(ErrorCode.USER_DOES_NOT_FOUND,
                                  f"メールアドレス {email_address.text} のユーザーが見つかりませんでした。")

        # メールアドレス検証が終わっていない場合は、確認メールを再送信する
        if not user.is_verified():
            # 認証メール送信のためにサブスクライバを登録
            DomainEventPublisher.instance().subscribe(VerificationTokenGeneratedSubscriber())

            user.generate(Token.Type.VERIFICATION)
            self.user_repository.add(user)
            raise SystemException(ErrorCode.USER_IS_NOT_VERIFIED,
                                  "メールアドレスの認証が完了していません。認証メールを送信しました。")

        return UserDpo(user, [], [])
