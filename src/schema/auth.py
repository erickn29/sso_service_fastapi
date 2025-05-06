from pydantic import BaseModel


class LoginSchema(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenVerifyInputSchema(BaseModel):
    token: str


class TokenVerifyOutputSchema(BaseModel):
    is_valid: bool
