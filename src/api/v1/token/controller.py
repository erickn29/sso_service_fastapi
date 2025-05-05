from fastapi import APIRouter, HTTPException

from schema.auth import LoginSchema, TokenSchema
from service.auth import AuthService


router = APIRouter()


@router.post("/login/", response_model=TokenSchema)
async def login(login_data: LoginSchema):
    if tokens := await AuthService().get_tokens(login_data):
        return TokenSchema(**tokens)
    raise HTTPException(400, "Неверный логин или пароль")


@router.get("/token/")
async def get_access_token():
    pass
