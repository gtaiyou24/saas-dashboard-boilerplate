from typing import Annotated

from fastapi import Form


class AuthorizationCodeForm:
    def __init__(
        self,
        code: Annotated[str, Form()],
        redirect_uri: Annotated[str, Form()],
        code_verifier: Annotated[str, Form()],
        grant_type: Annotated[str, Form()],
    ):
        self.code = code
        self.redirect_uri = redirect_uri
        self.code_verifier = code_verifier
        self.grant_type = grant_type

    # def make_google_command(self,
    #                         client_id: str,
    #                         client_secret: str,
    #                         user_dpo: UserDpo | None = None) -> AuthenticateAccountCommand:
    #     # 一時コード指定で Google からアクセストークンを取得する
    #     # https://developers.google.com/identity/protocols/oauth2/web-server?hl=ja#httprest_3
    #     response = requests.post(
    #         "https://oauth2.googleapis.com/token",
    #         headers={"Content-Type": "application/x-www-form-urlencoded"},
    #         data=urllib.parse.urlencode({
    #             "client_id": client_id,
    #             "client_secret": client_secret,
    #             "code": self.code,
    #             "grant_type": "authorization_code",
    #             "redirect_uri": self.redirect_uri,
    #             "code_verifier": self.code_verifier
    #         })
    #     )
    #     if not response.ok:
    #         raise RuntimeError(f"Google 認証に失敗しました。アクセストークンを取得できませんでした。{response.json()}")
    #     token = response.json()
    #
    #     response = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
    #                             headers={"Content-Type": "application/json"},
    #                             params={"access_token": token['access_token']})
    #     if not response.ok:
    #         raise RuntimeError("Google 認証に失敗しました。ユーザー情報の取得に失敗しました。")
    #     userinfo = response.json()
    #
    #     return AuthenticateAccountCommand.google(token, userinfo, user_dpo)
