from __future__ import annotations

from injector import inject

from authority.domain.model.tenant import TenantId, Tenant
from authority.domain.model.user import UserId
from authority.port.adapter.persistence.repository.mysql.tenant.driver import TenantsTableRow, MembersTableRow
from common.application import UnitOfWork
from common.port.adapter.persistence.repository.mysql import MySQLUnitOfWork


class DriverManagerTenant:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work: MySQLUnitOfWork = unit_of_work

    def find_by_id(self, tenant_id: TenantId) -> Tenant | None:
        with self.__unit_of_work.query() as q:
            optional: TenantsTableRow | None = q.query(TenantsTableRow).get(tenant_id.value)
            return optional.to_entity() if optional else None

    def find_one_by(self, **kwargs) -> Tenant | None:
        with self.__unit_of_work.query() as q:
            optional: TenantsTableRow | None = q.query(TenantsTableRow).filter_by(**kwargs).one_or_none()
            if optional is None:
                return None
            return optional.to_entity()

    def find_all_by(self, **kwargs) -> list[Tenant]:
        with self.__unit_of_work.query() as q:
            all: list[TenantsTableRow] = q.query(TenantsTableRow).filter_by(**kwargs).all()
            return [e.to_entity() for e in all]

    def find_all_by_user_id(self, user_id: UserId) -> list[Tenant]:
        with self.__unit_of_work.query() as q:
            all: list[MembersTableRow] = q.query(MembersTableRow).filter_by(user_id=user_id.value).all()
            return [e.tenant.to_entity() for e in all]

    def upsert(self, tenant: Tenant) -> None:
        exists = self.__unit_of_work.session().query(TenantsTableRow).filter_by(id=tenant.id.value).exists()
        if self.__unit_of_work.session().query(exists).scalar():
            self.update(tenant)
        else:
            self.insert(tenant)

    def insert(self, tenant: Tenant) -> None:
        self.__unit_of_work.persist(TenantsTableRow.create(tenant))

    def update(self, tenant: Tenant) -> None:
        optional: TenantsTableRow | None = self.__unit_of_work.session().query(TenantsTableRow).get(tenant.id.value)
        if optional is None:
            raise Exception(f'{TenantsTableRow.__tablename__}.{tenant.id.value} が存在しないため、更新できません。')

        self.__unit_of_work.delete(*optional.invitations)
        self.__unit_of_work.delete(*optional.members)
        self.__unit_of_work.flush()

        optional.update(tenant)

    def delete(self, tenant: Tenant) -> None:
        optional: TenantsTableRow | None = self.__unit_of_work.session().query(TenantsTableRow).get(tenant.id.value)
        if optional is None:
            return None

        self.__unit_of_work.delete(*optional.invitations)
        self.__unit_of_work.delete(*optional.members)
        self.__unit_of_work.flush()

        self.__unit_of_work.delete(optional)
