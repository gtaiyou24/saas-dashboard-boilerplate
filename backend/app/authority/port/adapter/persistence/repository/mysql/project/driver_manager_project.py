from __future__ import annotations

from injector import inject

from authority.domain.model.tenant.project import ProjectId, Project
from authority.port.adapter.persistence.repository.mysql.project.driver import ProjectsTableRow
from common.application import UnitOfWork
from common.port.adapter.persistence.repository.mysql import MySQLUnitOfWork


class DriverManagerProject:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work: MySQLUnitOfWork = unit_of_work

    def find_by_id(self, project_id: ProjectId) -> Project | None:
        with self.__unit_of_work.query() as q:
            optional: ProjectsTableRow | None = q.query(ProjectsTableRow).get(project_id.value)
            return optional.to_entity() if optional else None

    def find_by_ids(self, *project_id: ProjectId) -> Project | None:
        with self.__unit_of_work.query() as q:
            optional: ProjectsTableRow | None = q.query(ProjectsTableRow).get(project_id.value)
            return optional.to_entity() if optional else None

    def find_one_by(self, **kwargs) -> Project | None:
        with self.__unit_of_work.query() as q:
            optional: ProjectsTableRow | None = q.query(ProjectsTableRow).filter_by(**kwargs).one_or_none()
            return optional.to_entity() if optional else None

    def find_all_by(self, **kwargs) -> list[Project]:
        with self.__unit_of_work.query() as q:
            all: list[ProjectsTableRow] = q.query(ProjectsTableRow).filter_by(**kwargs).all()
            return [e.to_entity() for e in all]

    def upsert(self, project: Project) -> None:
        exists = self.__unit_of_work.session().query(ProjectsTableRow).filter_by(id=project.id.value).exists()
        if self.__unit_of_work.session().query(exists).scalar():
            self.update(project)
        else:
            self.insert(project)

    def insert(self, project: Project) -> None:
        self.__unit_of_work.persist(ProjectsTableRow.create(project))

    def update(self, project: Project) -> None:
        optional: ProjectsTableRow | None = self.__unit_of_work.session().query(ProjectsTableRow).get(project.id.value)
        if optional is None:
            raise Exception(f'{ProjectsTableRow.__tablename__}.{project.id.value} が存在しないため、更新できません。')

        optional.update(project)

    def delete(self, project: Project) -> None:
        optional: ProjectsTableRow | None = self.__unit_of_work.session().query(ProjectsTableRow).get(project.id.value)
        if optional is None:
            return None

        self.__unit_of_work.delete(optional)
