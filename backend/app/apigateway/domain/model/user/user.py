from dataclasses import dataclass

from apigateway.domain.model.user import UserId


@dataclass(init=False, unsafe_hash=True, frozen=True)
class User:
    id: UserId

    def __init__(self, id: UserId):
        assert id, "ユーザーIDは必須です。"
        super().__setattr__("id", id)

    def login(self) -> ("AccessToken", "RefreshToken"):
        # 巡回参照エラーにならないようにここでインポートする
        from apigateway.domain.model.token import AccessToken

        return AccessToken.generate(self.id)
