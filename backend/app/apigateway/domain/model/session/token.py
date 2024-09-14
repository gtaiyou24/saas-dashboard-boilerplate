from __future__ import annotations

import datetime
import enum
import uuid
from dataclasses import dataclass
from typing import Literal

import pytz


@dataclass(init=True, unsafe_hash=False, frozen=True)
class Token:
    """トークン"""

    class Type(enum.Enum):
        ACCESS = ("アクセストークン", 60)
        REFRESH = ("リフレッシュトークン", 60 * 24 * 7)

        def __init__(self, ja: str, expiration_minutes: int):
            self.ja = ja
            self.expiration_minutes = expiration_minutes

        def generate(self) -> Token:
            """トークンを生成します。
            このメソッドでは、各トークンの生成ロジックを記述しています。
            今後トークンの生成ロジックが複雑になってきたら、ファクトリクラスなどに切り出すこと。
            """
            tz = pytz.timezone('Asia/Tokyo')
            published_at = datetime.datetime.now().astimezone(tz)
            expires_at = published_at + datetime.timedelta(minutes=self.expiration_minutes)
            return Token(self, str(uuid.uuid4()), published_at, expires_at.astimezone(tz))

    type: Type
    value: str
    published_at: datetime.datetime
    expires_at: datetime.datetime

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: Token):
        if not isinstance(other, Token):
            return False
        return self.value == other.value

    @staticmethod
    def generate(type: Literal['ACCESS', 'REFRESH']) -> Token:
        return Token.Type[type].generate()

    def is_(self, type: Token.Type) -> bool:
        return self.type == type

    def has_expired(self) -> bool:
        tz = pytz.timezone('Asia/Tokyo')
        return self.expires_at.astimezone(tz) < datetime.datetime.now().astimezone(tz)

    def is_published_after(self, published_at: datetime.datetime) -> bool:
        tz = pytz.timezone('Asia/Tokyo')
        return self.published_at.astimezone(tz) > published_at.astimezone(tz)
