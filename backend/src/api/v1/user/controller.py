from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from deps.auth import is_admin_or_service
from schema.user import (
    UserDeleteSchema,
    UserInputSchema,
    UserOutputSchema,
    UserUpdateInputSchema,
)
from service.user import UserServiceV1


router = APIRouter(dependencies=[Depends(is_admin_or_service)])


@router.post("/", response_model=UserOutputSchema, status_code=201)
async def create_user(user: UserInputSchema):
    """Create user"""
    return await UserServiceV1().create(user)


@router.get("/{user_id}/", response_model=UserOutputSchema, status_code=200)
async def read_user(user_id: UUID):
    """Get user"""
    if user := await UserServiceV1().find_by_id(user_id):
        return user
    raise HTTPException(404)


@router.put("/{user_id}/", response_model=UserOutputSchema, status_code=201)
async def update_user(user_id: UUID, user: UserUpdateInputSchema):
    """Update user"""
    if user_obj := await UserServiceV1().update(user_id, **user.model_dump()):
        return user_obj
    raise HTTPException(404)


@router.delete("/{user_id}/", response_model=UserDeleteSchema, status_code=201)
async def delete_user(user_id: UUID):
    """Deactivate user"""
    user = await UserServiceV1().delete(user_id)
    return {"success": bool(user)}
