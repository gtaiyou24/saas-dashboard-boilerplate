from __future__ import annotations

from datetime import datetime

from sqlalchemy import UniqueConstraint, ForeignKey, Integer, String, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from authority.domain.model.mail import EmailAddress
from authority.domain.model.tenant import Tenant, Invitation
from common.port.adapter.persistence.repository.mysql import DataBase


class InvitationsTableRow(DataBase):
    __tablename__ = "invitations"
    __table_args__ = (
        (UniqueConstraint("code", name=f"uix_{__tablename__}_1")),
        (Index(f"idx_{__tablename__}_1", 'tenant_id')),
        (Index(f"idx_{__tablename__}_2", 'code')),
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False, autoincrement=True)
    tenant_id: Mapped[str] = mapped_column(
        ForeignKey('tenants.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    code: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    email_address: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="トークン発行日時")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="トークン失効日時")

    tenant = relationship("TenantsTableRow", back_populates="invitations")

    @staticmethod
    def create(tenant: Tenant) -> list[InvitationsTableRow]:
        return [
            InvitationsTableRow(
                tenant_id=tenant.id.value,
                code=invitation.code,
                email_address=invitation.to,
                published_at=invitation.starting_on,
                expires_at=invitation.until
            ) for invitation in tenant.invitations if invitation.is_available()
        ]

    def to_value(self) -> Invitation:
        return Invitation(self.code, EmailAddress(self.email_address), self.published_at, self.expires_at)
