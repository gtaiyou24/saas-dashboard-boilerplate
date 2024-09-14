from __future__ import annotations

from injector import singleton, inject

from authority.domain.model.tenant import Tenant, TenantId
from authority.domain.model.user import UserId
from authority.port.adapter.persistence.repository.mysql.tenant import DriverManagerTenant


@singleton
class CacheLayerTenant:
    """キャッシュを保持するクラス"""
    values = dict()

    # 60秒 × 15分
    __TTL = 60 * 15

    @inject
    def __init__(self, driver_manager_tenant: DriverManagerTenant):
        self.__driver_manager_tenant = driver_manager_tenant

    def cache_or_origin(self, tenant_id: TenantId) -> Tenant | None:
        key = f'id-{tenant_id.value}'
        if key in self.values.keys():
            return self.values[key]

        optional = self.__driver_manager_tenant.find_by_id(tenant_id)
        self.values[key] = optional
        return self.values[key]

    def caches_or_origins(self, *tenant_id: TenantId) -> list[Tenant] | None:
        return self.__driver_manager_tenant.find_by_ids(*tenant_id)

    def caches_or_origins_with_user_id(self, user_id: UserId) -> list[Tenant]:
        return self.__driver_manager_tenant.find_all_by_user_id(user_id)

    def set(self, tenant: Tenant) -> None:
        self.__driver_manager_tenant.upsert(tenant)
        # キャッシュを更新する
        self.values[f'id-{tenant.id.value}'] = tenant

    def delete(self, tenant: Tenant) -> None:
        self.__driver_manager_tenant.delete(tenant)
        # キャッシュを更新する
        self.values[f'id-{tenant.id.value}'] = None
