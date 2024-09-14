from __future__ import annotations

import uuid
from typing import override

from authority.domain.model.tenant import TenantRepository, Tenant, TenantId
from authority.domain.model.user import UserId


class InMemTenantRepository(TenantRepository):
    values: set[Tenant] = set()

    @override
    def next_identity(self) -> TenantId:
        return TenantId(str(uuid.uuid4()))

    @override
    def add(self, tenant: Tenant) -> None:
        self.values.add(tenant)

    @override
    def remove(self, tenant: Tenant) -> None:
        self.values.remove(tenant)

    @override
    def get(self, tenant_id: TenantId) -> Tenant | None:
        for e in self.values:
            if e.id == tenant_id:
                return e
        return None

    @override
    def tenants_with_user_id(self, user_id: UserId) -> set[Tenant]:
        tenants = set()
        for e in self.values:
            for m in e.members:
                if m.user_id == user_id:
                    tenants.add(e)
                    break
        return tenants
