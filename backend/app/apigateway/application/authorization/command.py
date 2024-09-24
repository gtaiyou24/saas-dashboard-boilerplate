from __future__ import annotations

import abc
from dataclasses import dataclass
from enum import Enum


@dataclass(init=True, unsafe_hash=True, frozen=True)
class AuthenticateCommand(abc.ABC):
    class OAuthType(Enum):
        CREDENTIAL = 'email_password'
        GOOGLE = 'google'
        GITHUB = 'github'

    oauth_type: OAuthType


class AuthenticateEmailPasswordCommand(AuthenticateCommand):
    email_address: str
    plain_password: str
    oauth_type = AuthenticateCommand.OAuthType.CREDENTIAL

    def __str__(self):
        return f"{'email_address': {self.email_address}, 'plain_password': {self.plain_password[0:1]}...}"


@dataclass(init=True, unsafe_hash=True, frozen=True)
class AuthenticateAccountCommand(AuthenticateCommand):
    code: str
    redirect_uri: str
    code_verifier: str

    def __str__(self):
        return f"{'code': {self.code}, 'redirect_uri': {self.redirect_uri}, 'code_verifier': {self.code_verifier}}"


@dataclass(init=True, unsafe_hash=True, frozen=True)
class RefreshCommand:
    refresh_token: str


@dataclass(init=True, unsafe_hash=True, frozen=True)
class RevokeCommand:
    token: str
