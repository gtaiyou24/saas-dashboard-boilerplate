import abc

from authority.domain.model.tenant import TenantId
from authority.domain.model.tenant.project import ProjectId, Project


class ProjectRepository(abc.ABC):
    @abc.abstractmethod
    def next_identity(self) -> ProjectId:
        pass

    @abc.abstractmethod
    def add(self, project: Project) -> None:
        pass

    @abc.abstractmethod
    def projects_with_tenant_id(self, tenant_id: TenantId) -> set[Project]:
        pass
