from fastapi import APIRouter

from schema.user import UserInputSchema, UserOutputSchema
from service.user import UserServiceV1


router = APIRouter()


@router.post("", response_model=UserOutputSchema)
async def create(user: UserInputSchema):
    """Создание пользователя"""
    user_service = UserServiceV1()
    return await user_service.create(user)
