from injector import singleton, inject

from authority.application.identity.command import RegisterUserCommand
from authority.application.identity.dpo import TenantDpo
from authority.application.identity.subscriber import UserProvisionedSubscriber
from authority.domain.model.mail import SendMailService, EmailAddress
from authority.domain.model.tenant import TenantRepository, Tenant
from authority.domain.model.tenant.project import ProjectRepository
from authority.domain.model.user import UserRepository, User
from common.application import transactional
from common.domain.model import DomainEventPublisher


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
        DomainEventPublisher.instance().subscribe(UserProvisionedSubscriber())

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
