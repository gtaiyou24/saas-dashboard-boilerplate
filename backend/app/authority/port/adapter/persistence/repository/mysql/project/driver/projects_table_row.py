from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from authority.domain.model.tenant import TenantId
from authority.domain.model.tenant.project import Project, ProjectId
from common.port.adapter.persistence.repository.mysql import DataBase


class ProjectsTableRow(DataBase):
    __tablename__ = "projects"
    __table_args__ = (
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False)
    tenant_id: Mapped[str] = mapped_column(ForeignKey('tenants.id', onupdate='CASCADE', ondelete='CASCADE'),
                                           nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(),
                                                 onupdate=func.now())

    @staticmethod
    def create(project: Project) -> ProjectsTableRow:
        return ProjectsTableRow(id=project.id.value, tenant_id=project.tenant_id.value, name=project.name)

    def update(self, project: Project) -> None:
        self.name = project.name

    def to_entity(self) -> Project:
        return Project(id=ProjectId(self.id), tenant_id=TenantId(self.tenant_id), name=self.name,)
