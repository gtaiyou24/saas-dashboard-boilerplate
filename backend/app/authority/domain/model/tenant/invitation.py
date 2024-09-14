from __future__ import annotations

import datetime
import uuid
from dataclasses import dataclass

import pytz

from authority.domain.model.mail import EmailAddress


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Invitation:
    """招待状"""
    code: str
    to: EmailAddress
    starting_on: datetime.datetime
    until: datetime.datetime

    @staticmethod
    def generate(mail: EmailAddress) -> Invitation:
        """メールアドレス指定で招待状を生成します"""
        tz = pytz.timezone('Asia/Tokyo')
        starting_on = datetime.datetime.now().astimezone(tz)
        expires_at = starting_on + datetime.timedelta(hours=1)  # 有効時間を1時間にしています
        return Invitation(str(uuid.uuid4()), mail, starting_on, expires_at.astimezone(tz))

    def is_available(self) -> bool:
        """招待状が有効か判定できる"""
        tz = pytz.timezone('Asia/Tokyo')
        now = datetime.datetime.now().astimezone(tz)
        return self.starting_on.astimezone(tz) <= now <= self.until.astimezone(tz)
