from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from authority.domain.model.tenant import Tenant, TenantId
from authority.port.adapter.persistence.repository.mysql.tenant.driver import InvitationsTableRow, MembersTableRow
from common.port.adapter.persistence.repository.mysql import DataBase


class TenantsTableRow(DataBase):
    __tablename__ = "tenants"
    __table_args__ = (
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(),
                                                 onupdate=func.now())

    invitations: Mapped[list[InvitationsTableRow]] = relationship(back_populates="tenant", lazy='joined')
    members: Mapped[list[MembersTableRow]] = relationship(back_populates="tenant", lazy='joined')

    @staticmethod
    def create(tenant: Tenant) -> TenantsTableRow:
        return TenantsTableRow(
            id=tenant.id.value,
            name=tenant.name,
            invitations=InvitationsTableRow.create(tenant),
            members=MembersTableRow.create(tenant)
        )

    def update(self, tenant: Tenant) -> None:
        self.name = tenant.name
        self.invitations = InvitationsTableRow.create(tenant)
        self.members = MembersTableRow.create(tenant)

    def to_entity(self) -> Tenant:
        return Tenant(
            id=TenantId(self.id),
            name=self.name,
            invitations={tr.to_value() for tr in self.invitations},
            members={tr.to_value() for tr in self.members}
        )
