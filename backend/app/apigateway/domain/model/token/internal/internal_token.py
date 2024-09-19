from __future__ import annotations

import datetime
import time
import uuid
from dataclasses import dataclass
from typing import Any

import pytz

from apigateway.domain.model.token.internal.claim import Name, Claim
from apigateway.domain.model.user import User


type ClaimName = {e.name for e in Name}


@dataclass(init=True, unsafe_hash=True, frozen=True)
class InternalToken:
    """内部通信用トークン

    詳細は、doc/INTERNAL_TOKEN.md を参照してください。
    """
    claims: set[Claim]

    @property
    def payload(self) -> dict[str, Any]:
        return {claim.name: claim.value for claim in self.claims}

    @staticmethod
    def generate(user: User) -> InternalToken:
        internal_token_id = str(uuid.uuid4())
        tz = pytz.timezone('Asia/Tokyo')
        now = datetime.datetime.now().astimezone(tz)
        exp = now + datetime.timedelta(seconds=10)
        return InternalToken({
            Name.ISSUER.make("api-gateway"),  # マイクロサービス化した場合は、API Gateway の URLとなる
            Name.SUBJECT.make("internal-token"),
            Name.ISSUED_AT.make(int(time.time())),
            Name.NOT_BEFORE.make(int(time.time())),
            Name.EXPIRATION_TIME.make(int(round(exp.timestamp()))),
            Name.JWT_ID.make(internal_token_id),
            Name.USER_ID.make(user.id.value)
        })

    def add_audience(self, value: str) -> InternalToken:
        claims = self.claims
        claims.add(Name.AUDIENCE.make(value))
        return InternalToken(claims)
