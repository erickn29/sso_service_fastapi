from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from schema.auth import (
    LoginSchema,
    TokenSchema,
    TokenVerifyInputSchema,
    TokenVerifyOutputSchema,
)
from service.auth import AuthService


router = APIRouter()


@router.post("/login/", response_model=TokenSchema)
async def login(login_data: LoginSchema):
    """Get access and refresh tokens"""
    if tokens := await AuthService().get_tokens(login_data):
        return TokenSchema(**tokens)
    raise HTTPException(400, "Неверный логин или пароль")


@router.get("/token/", response_model=TokenSchema)
async def get_access_token(request: Request):
    """Refresh access token"""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(400, "Не найден refresh token")
    access_token = AuthService().refresh_access_token(refresh_token)
    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/token/verify/", response_model=TokenVerifyOutputSchema)
async def verify_token(schema: TokenVerifyInputSchema):
    """Check payload and token expires time"""
    is_valid = AuthService().verify_token(schema.token)
    return TokenVerifyOutputSchema(is_valid=is_valid)
