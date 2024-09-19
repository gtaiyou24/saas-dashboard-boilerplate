from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Claim:
    _name: Name
    value: str | int | dict | list

    @staticmethod
    def make(name: Name, value: str | int | dict | list) -> Claim:
        return Claim(name, value)

    @property
    def name(self) -> str:
        return self._name.value


class Name(Enum):
    ISSUER = 'iss'  # JWTの発行者を表す識別子(issuer)。
    SUBJECT = 'sub'  # ユーザーの識別子(subject)。通常ユーザーのIDとなる。
    AUDIENCE = 'aud'  # JWTを利用するクライアント識別子で最初にリクエストを受信するモジュール名ないしはマイクロサービス名(audience)。
    EXPIRATION_TIME = 'exp'  # JWT の有効期限のタイムスタンプ(expiration)
    NOT_BEFORE = 'nbf'  # JWT が有効となる日時のタイムスタンプ(not before)
    ISSUED_AT = 'iat'  # JWT の発行日時のタイムスタンプ(issued at)
    JWT_ID = 'jti'  # JWT の一意な識別子
    USER_ID = 'user_id'

    def make(self, value: str | int | dict | list) -> Claim:
        return Claim(self, value)
