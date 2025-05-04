from fastapi import APIRouter

from schema.user import UserInputSchema, UserOutputSchema
from service.user import UserServiceV1


router = APIRouter()


@router.post("/", response_model=UserOutputSchema, status_code=201)
async def create_user(user: UserInputSchema):
    """Создание пользователя"""
    user_service = UserServiceV1()
    return await user_service.create(user)
