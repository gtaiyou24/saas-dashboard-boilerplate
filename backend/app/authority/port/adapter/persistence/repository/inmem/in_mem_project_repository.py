import uuid
from typing import override

from authority.domain.model.tenant import TenantId
from authority.domain.model.tenant.project import ProjectRepository, Project, ProjectId


class InMemProjectRepository(ProjectRepository):
    projects: set[Project] = set()

    @override
    def next_identity(self) -> ProjectId:
        return ProjectId(str(uuid.uuid4()))

    @override
    def add(self, project: Project) -> None:
        self.projects.add(project)

    @override
    def projects_with_tenant_id(self, tenant_id: TenantId) -> set[Project]:
        pass
