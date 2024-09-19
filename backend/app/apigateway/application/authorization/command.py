from __future__ import annotations

from dataclasses import dataclass


@dataclass(init=True, unsafe_hash=True, frozen=True)
class AuthenticateCommand:
    email_address: str
    plain_password: str | None


@dataclass(init=True, unsafe_hash=True, frozen=True)
class RefreshCommand:
    refresh_token: str


@dataclass(init=True, unsafe_hash=True, frozen=True)
class RevokeCommand:
    token: str
