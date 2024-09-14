from __future__ import annotations

from enum import Enum

from sqlalchemy import UniqueConstraint, Index, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from authority.domain.model.tenant import Tenant
from authority.domain.model.tenant.member import Member
from authority.domain.model.user import UserId
from common.port.adapter.persistence.repository.mysql import DataBase, EnumType

MemberRoleField = Enum("Member.Role", " ".join([e.name for e in Member.Role]))


class MembersTableRow(DataBase):
    __tablename__ = "members"
    __table_args__ = (
        (UniqueConstraint("tenant_id", "user_id", name=f"uix_{__tablename__}_1")),
        (Index(f"idx_{__tablename__}_1", 'tenant_id')),
        (Index(f"idx_{__tablename__}_2", 'user_id')),
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False, autoincrement=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey('tenants.id', onupdate='CASCADE', ondelete='CASCADE'),
                                           nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
                                         nullable=False)
    role: Mapped[int] = mapped_column(EnumType(enum_class=MemberRoleField), nullable=False,
                                      comment='1=管理者, 2=編集者, 3=閲覧者')

    tenant = relationship("TenantsTableRow", back_populates="members", lazy='joined')

    @staticmethod
    def create(tenant: Tenant) -> list[MembersTableRow]:
        return [
            MembersTableRow(
                tenant_id=tenant.id.value,
                user_id=member.user_id.value,
                role=MemberRoleField[member.role.name]
            ) for member in tenant.members
        ]

    def to_value(self) -> Member:
        return Member(UserId(self.user_id), Member.Role[self.role.name])
