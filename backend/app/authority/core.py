from typing import override

from di import DIContainer, DI
from fastapi import APIRouter

from authority.domain.model.mail import SendMailService
from authority.domain.model.tenant import TenantRepository
from authority.domain.model.tenant.project import ProjectRepository
from authority.domain.model.user import EncryptionService, UserRepository
from authority.port.adapter.persistence.repository.inmem import InMemTenantRepository, InMemUserRepository, \
    InMemProjectRepository
from authority.port.adapter.persistence.repository.mysql.project import MySQLProjectRepository
from authority.port.adapter.persistence.repository.mysql.tenant import MySQLTenantRepository
from authority.port.adapter.persistence.repository.mysql.user import MySQLUserRepository
from authority.port.adapter.resource.user import UserResource
from authority.port.adapter.service.mail import SendMailServiceImpl
from authority.port.adapter.service.mail.adapter import MailDeliveryAdapter
from authority.port.adapter.service.mail.adapter.gmail import GmailAdapter
from authority.port.adapter.service.mail.adapter.mailhog import MailHogAdapter
from authority.port.adapter.service.mail.adapter.sendgrid import SendGridAdapter
from authority.port.adapter.service.mail.adapter.stub import MailDeliveryAdapterStub
from authority.port.adapter.service.user import EncryptionServiceImpl
from common.core import AppModule


class Authority(AppModule):
    @override
    def startup(self) -> None:
        DIContainer.instance().register(
            # Persistence
            DI.of(ProjectRepository, {"MySQL": MySQLProjectRepository}, InMemProjectRepository),
            DI.of(TenantRepository, {"MySQL": MySQLTenantRepository}, InMemTenantRepository),
            DI.of(UserRepository, {"MySQL": MySQLUserRepository}, InMemUserRepository),
            # Service
            DI.of(SendMailService, {}, SendMailServiceImpl),
            DI.of(EncryptionService, {}, EncryptionServiceImpl),
            # Adapter
            DI.of(
                MailDeliveryAdapter,
                {"SendGrid": SendGridAdapter, "MailHog": MailHogAdapter, "Gmail": GmailAdapter},
                MailDeliveryAdapterStub
            ),
        )

    @override
    def shutdown(self) -> None:
        pass

    @override
    @property
    def router(self) -> APIRouter:
        router = APIRouter(tags=["Authority"])
        router.include_router(UserResource().router)
        return router
