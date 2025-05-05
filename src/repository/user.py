from uuid import UUID

from model import User
from repository.base import BaseRepo
from schema.user import UserInputSchema, UserOutputSchema


class UserRepoV1(BaseRepo):
    model = User

    async def create_user(self, data: UserInputSchema) -> UserOutputSchema:
        """Create user"""
        obj = await self.create(**data.model_dump())
        return UserOutputSchema.model_validate(obj)

    async def update_user(self, user_id: UUID, **data) -> UserOutputSchema | None:
        """Update user"""
        obj = await self.find(id=user_id)
        if not obj:
            return None
        updated_obj = await self.update(obj, **data)
        return UserOutputSchema.model_validate(updated_obj)

    async def find_user(self, user_id: UUID) -> UserOutputSchema | None:
        """Find user"""
        obj = await self.find(id=user_id, is_active=True)
        if not obj:
            return None
        return UserOutputSchema.model_validate(obj)

    async def delete_user(self, user_id: UUID) -> UserOutputSchema | None:
        """Deactivate user"""
        obj = await self.find(id=user_id)
        if not obj:
            return None
        return await self.update(obj, **{"is_active": False})
