from fastapi import APIRouter

from schema.auth import LoginSchema, TokenSchema
from service.auth import AuthService


router = APIRouter()


@router.post("/login/", response_model=TokenSchema)
async def login(login_data: LoginSchema):
    return await AuthService().get_tokens(login_data)


@router.get("/token/")
async def get_access_token():
    pass
