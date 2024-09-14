from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from authority.domain.model.user import UserId


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Member:
    """テナントに所属しているメンバー"""
    class Role(Enum):
        ADMIN = '管理者'
        EDITOR = '編集者'
        READER = '閲覧者'

    user_id: UserId
    role: Role
