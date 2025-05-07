from pydantic import BaseModel, Field


class LoginSchema(BaseModel):
    email: str = Field(min_length=5, max_length=320)
    password: str = Field(min_length=8)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenVerifyInputSchema(BaseModel):
    token: str


class TokenVerifyOutputSchema(BaseModel):
    is_valid: bool
