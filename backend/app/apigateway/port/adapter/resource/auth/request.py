from pydantic import BaseModel, Field


class RegisterTenantRequest(BaseModel):
    username: str = Field(title="ユーザー名")
    email_address: str = Field(title="メールアドレス")
    password: str = Field(title="パスワード")


class OAuth2PasswordRequest(BaseModel):
    email_address: str = Field(title="メールアドレス")
    password: str = Field(title="パスワード")


class ForgotPasswordRequest(BaseModel):
    email_address: str = Field(title="メールアドレス")


class ResetPasswordRequest(BaseModel):
    token: str = Field(title="パスワードリセットトークン")
    password: str = Field(title="パスワード")
