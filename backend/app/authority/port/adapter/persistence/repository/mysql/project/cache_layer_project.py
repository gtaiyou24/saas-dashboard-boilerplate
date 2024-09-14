from __future__ import annotations

from injector import singleton, inject

from authority.domain.model.tenant import TenantId
from authority.domain.model.tenant.project import Project, ProjectId
from authority.port.adapter.persistence.repository.mysql.project import DriverManagerProject


@singleton
class CacheLayerProject:
    """キャッシュを保持するクラス"""
    values = dict()

    # 60秒 × 15分
    __TTL = 60 * 15

    @inject
    def __init__(self, driver_manager_project: DriverManagerProject):
        self.__driver_manager_project = driver_manager_project

    def cache_or_origin(self, project_id: ProjectId) -> Project | None:
        key = f'id-{project_id.value}'
        if key in self.values.keys():
            return self.values[key]

        optional = self.__driver_manager_project.find_by_id(project_id)
        self.values[key] = optional
        return self.values[key]

    def caches_or_origins(self, *project_id: ProjectId) -> list[Project] | None:
        return self.__driver_manager_project.find_by_id(*project_id)

    def caches_or_origins_with_tenant_id(self, tenant_id: TenantId) -> list[Project]:
        return self.__driver_manager_project.find_all_by(tenant_id=tenant_id.value)

    def set(self, project: Project) -> None:
        self.__driver_manager_project.upsert(project)
        # キャッシュを更新する
        self.values[f'id-{project.id.value}'] = project

    def delete(self, project: Project) -> None:
        self.__driver_manager_project.delete(project)
        # キャッシュを更新する
        self.values[f'id-{project.id.value}'] = None
