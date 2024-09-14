from __future__ import annotations

from dataclasses import dataclass

from apigateway.domain.model.session import SessionId, Token
from authority.domain.model.user import UserId
from common.exception import SystemException, ErrorCode


@dataclass(init=True, unsafe_hash=False, frozen=False)
class Session:
    """セッション"""
    id: SessionId
    user_id: UserId
    tokens: set[Token]

    def __hash__(self):
        return hash(self.id.value)

    def __eq__(self, other: Session):
        if not isinstance(other, Session):
            return False
        return self.id == other.id

    @staticmethod
    def publish(id: SessionId, user_id: UserId) -> Session:
        """セッションを発行"""
        return Session(id, user_id, {Token.generate('ACCESS'), Token.generate('REFRESH')})

    def refresh(self, refresh_value: str) -> None:
        """セッションを更新

        フロント側からAPIにトークンをリフレッシュした後に何かしらの理由で新しいトークンをクッキーに保存できないケースがある。
        その場合、フロント側では古いアクセストークンとリフレッシュトークンが残り続け、古いリフレッシュトークンでリクエストし続ける現象があります。
        そのため、バックエンド側では古いアクセストークンは削除するが、リフレッシュトークンは削除しないようにして、
        フロントエンド側で再度リフレッシュできるようにする。
        """
        refresh_token = self.token_with(refresh_value)
        if refresh_token is None or refresh_token.has_expired():
            raise SystemException(
                ErrorCode.VALID_TOKEN_DOES_NOT_EXISTS, f'{refresh_token} は無効なリフレッシュトークンです。')

        # 指定されたリフレッシュトークンが古い、且つ最新のアクセストークンが有効な場合は、新しくトークンを生成せずに現状の最新トークンを返す
        latest_refresh_token = self.latest_token_of(Token.Type.REFRESH)
        latest_access_token = self.latest_token_of(Token.Type.ACCESS)
        if refresh_token != latest_refresh_token and not latest_access_token.has_expired():
            return

        new_tokens = {Token.generate('ACCESS'), Token.generate('REFRESH')}
        for old_token in self.tokens:
            if old_token.is_(Token.Type.REFRESH) and not old_token.has_expired():
                # 有効なリフレッシュトークンのみセッションに残す
                new_tokens.add(old_token)

        self.tokens = new_tokens

    def token_with(self, value: str) -> Token | None:
        """トークンの値指定で該当トークンを取得できる"""
        for e in self.tokens:
            if e.value == value:
                return e
        return None

    def latest_token_of(self, type: Token.Type) -> Token | None:
        """トークンタイプ指定で最新の該当トークンを取得する"""
        latest_token = None
        for token in self.tokens:
            if not token.is_(type):
                continue
            if latest_token is None or token.is_published_after(latest_token.published_at):
                latest_token = token
        return latest_token

    def latest_access_token(self) -> Token | None:
        return self.latest_token_of(Token.Type.ACCESS)

    def latest_refresh_token(self) -> Token | None:
        return self.latest_token_of(Token.Type.REFRESH)
