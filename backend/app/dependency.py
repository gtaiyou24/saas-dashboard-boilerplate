from dataclasses import dataclass
from typing import Literal

from fastapi import Header
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@dataclass(init=True, unsafe_hash=True, frozen=True)
class CurrentUser:
    pass


@dataclass(frozen=True, eq=True)
class GetCurrentUser:
    """内部通信用トークンからアクセスユーザー情報を取得する

    Usage:

    def get(self, current_user: CurrentUser = Depends(GetCurrentUser(permit={'ADMIN'}))):
        ...
    """
    permit: set[Literal['OWNER', 'ADMIN', 'EDITOR', 'VIEWER']]

    def __call__(self, x_internal_token: str | None = Header()) -> CurrentUser:
        print(x_internal_token)
        # TODO: 内部通信用トークンを署名検証し、ユーザー情報を取得する
        # TODO: 取得したユーザー情報をもとに必要な権限を有しているのか確認する。もし必要な権限を持っていない場合は 403 とする。

    def __hash__(self) -> int:
        return hash(",".join(sorted(map(str, list(self.permit)))))
