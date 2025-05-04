from http.client import HTTPException
from uuid import UUID

from fastapi import APIRouter

from schema.user import UserInputSchema, UserOutputSchema
from service.user import UserServiceV1


router = APIRouter()


@router.post("/", response_model=UserOutputSchema, status_code=201)
async def create_user(user: UserInputSchema):
    """Создание пользователя"""
    return await UserServiceV1().create(user)


@router.get("/{user_id}/", response_model=UserOutputSchema, status_code=200)
async def read_user(user_id: UUID):
    """Получение пользователя"""
    if user := await UserServiceV1().find(user_id):
        return user
    raise HTTPException(404)
