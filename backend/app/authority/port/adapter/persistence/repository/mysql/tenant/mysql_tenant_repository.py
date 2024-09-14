from __future__ import annotations

import uuid
from typing import override

from injector import inject

from authority.domain.model.tenant import TenantRepository, Tenant, TenantId
from authority.domain.model.user import UserId
from authority.port.adapter.persistence.repository.mysql.tenant import CacheLayerTenant


class MySQLTenantRepository(TenantRepository):
    @inject
    def __init__(self, cache_layer_tenant: CacheLayerTenant):
        self.__cache_layer_tenant = cache_layer_tenant

    @override
    def next_identity(self) -> TenantId:
        return TenantId(str(uuid.uuid4()))

    @override
    def add(self, tenant: Tenant) -> None:
        self.__cache_layer_tenant.set(tenant)

    @override
    def remove(self, tenant: Tenant) -> None:
        self.__cache_layer_tenant.delete(tenant)

    @override
    def get(self, tenant_id: TenantId) -> Tenant | None:
        return self.__cache_layer_tenant.cache_or_origin(tenant_id)

    @override
    def tenants_with_user_id(self, user_id: UserId) -> list[Tenant]:
        return self.__cache_layer_tenant.caches_or_origins_with_user_id(user_id)
