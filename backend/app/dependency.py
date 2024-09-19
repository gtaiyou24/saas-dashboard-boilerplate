from dataclasses import dataclass
from typing import Literal

import jwt
from fastapi import Depends
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@dataclass(init=True, unsafe_hash=True, frozen=True)
class CurrentUser:
    id: str


@dataclass(frozen=True, eq=True)
class GetCurrentUser:
    """内部通信用トークンからアクセスユーザー情報を取得する

    Usage:

    def get(self, current_user: CurrentUser = Depends(GetCurrentUser(permit={'ADMIN'}))):
        ...
    """
    permit: set[Literal['ALL', 'OWNER', 'ADMIN', 'EDITOR', 'VIEWER']]

    def __call__(self, request: Request, token: str = Depends(oauth2_scheme)) -> CurrentUser:
        internal_token = request.headers.get('x-internal-token')
        # 内部通信用トークンを署名検証し、ユーザー情報を取得する
        payload = jwt.decode(
            internal_token,
            key="""-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEArgkhiVO4WGp8PUGUU1/a
XKri+E6NTvlxpHNMwSAs/ORU3MlomX/0fOEVW7qA/G0EEl8UgkfzuJhIpMrZP9EP
pEt4LZpcRwbYjdQYnImxWajbhmduZATmbdqjSVuA+NvIk2rIvtQ+aoVShjMetsU+
rwWUUYk164hY3fJezH7FSb2rVXzwWhEon30iSDKEE2o90aK8jSLheok5bPi0AMAs
FtRayuvuVWsKauW0FndvM6hsHTSYqs/D1VQFpuQCiz2mcElWwSP15GxQ4lBnUt/i
/n0yu41lDI58OlZwtkzejlgXc1hGy+8SEkIAxVqi0vzBhHiDvpsaymQDNqv9tkjI
ihuYPBT1Mfwomlox6f3LyDsh3EBTFKf6CnfhbYljNEwczrHSREHAkJwzB7NTtziv
Bu0K8ydi3t8XXvnLcq5xxcusjEOHx6a/7juoONJ2WRdV/WWEY1O16wP03oMqi5az
NIdlD3z2/inCDBKSOufsEUP6szCErQWHWt/S0xfuu3dAFpME8/ELVN+Vjnw7XsSW
YqYxaD/FwXEl9AgFGCWOOKChg6vim97ymE+p3ljeLbam7/jlQDFPYMxNAi3cI8is
NzzW09udb5TzqDxWb0+o7bdx+C043b3hQpZgszcDjKNE3BQGt51krFxZemNWRkhd
/MwSdUE8hTqT6jftw4VD+GUCAwEAAQ==
-----END PUBLIC KEY-----""",  # 一旦ハードコードで実装
            verify=True,
            audience=str(request.url),
            algorithms=["RS256"]
        )
        # TODO: 取得したユーザー情報をもとに必要な権限を有しているのか確認する。もし必要な権限を持っていない場合は 403 とする。
        return CurrentUser(id=payload['user_id'])

    def __hash__(self) -> int:
        return hash(",".join(sorted(map(str, list(self.permit)))))
