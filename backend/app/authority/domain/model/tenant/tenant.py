from __future__ import annotations

from dataclasses import dataclass

from authority.domain.model.mail import EmailAddress
from authority.domain.model.tenant import TenantId, Invitation
from authority.domain.model.tenant.member import Member
from authority.domain.model.tenant.project import Project, ProjectId
from authority.domain.model.user import User, UserId


@dataclass(init=True, eq=False)
class Tenant:
    id: TenantId
    name: str
    invitations: set[Invitation]
    members: set[Member]

    def __hash__(self):
        return hash(self.id.value)

    def __eq__(self, other: Tenant):
        if not isinstance(other, Tenant):
            return False
        return self.id == other.id

    @property
    def member_user_ids(self) -> list[UserId]:
        return [member.user_id for member in self.members]

    @staticmethod
    def provision(id: TenantId, name: str) -> Tenant:
        return Tenant(id, name, set(), set())

    def register_admin_member(self, user: User) -> Member:
        admin = Member(user.id, Member.Role.ADMIN)
        self.members.add(admin)
        return admin

    def create_project(self, project_id: ProjectId, name: str) -> Project:
        return Project(project_id, self.id, name)

    def invite(self, email_address: EmailAddress) -> Invitation:
        """メールアドレス指定でメンバーを招待する"""
        invitation = Invitation.generate(email_address)
        self.invitations.add(invitation)
        return invitation

    def withdraw_invitation(self, code: str) -> None:
        """招待状を破棄する"""
        self.invitations = set([e for e in self.invitations if e.code != code])

    def has_member(self, user_id: UserId) -> bool:
        """該当ユーザーがテナントに属しているか判定できる"""
        for member in self.members:
            if member.user_id == user_id:
                return True
        return False
