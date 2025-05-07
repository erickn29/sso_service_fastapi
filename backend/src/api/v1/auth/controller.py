from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from schema.auth import (
    LoginSchema,
    TokenSchema,
    TokenVerifyInputSchema,
    TokenVerifyOutputSchema,
)
from schema.user import UserVerifySchema
from service.auth import AuthService
from service.user import UserServiceV1


router = APIRouter()


@router.post("/login/", response_model=TokenSchema)
async def login(login_data: LoginSchema):
    """Get access and refresh tokens"""
    if tokens := await AuthService().get_tokens(login_data):
        return TokenSchema(**tokens)
    raise HTTPException(400, "Invalid email or password")


@router.get("/token/refresh/", response_model=TokenSchema)
async def get_access_token(request: Request):
    """Refresh access token"""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(400, "Refresh token not found")
    access_token = AuthService().refresh_access_token(refresh_token)
    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/token/verify/", response_model=TokenVerifyOutputSchema)
async def verify_token(schema: TokenVerifyInputSchema):
    """Check payload and token expiration time"""
    is_valid = AuthService().verify_token(schema.token)
    return TokenVerifyOutputSchema(is_valid=is_valid)


@router.get("/verify-email/{token}/", response_model=UserVerifySchema, status_code=200)
async def verify_email(token: UUID):
    """Verify email"""
    if is_verified := await UserServiceV1().verify_email(str(token)):
        return UserVerifySchema(success=is_verified)
    raise HTTPException(404)
