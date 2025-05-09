from uuid import UUID

from model import User
from repository.base import BaseRepo
from schema.user import UserInputSchema, UserOutputSchema


class UserRepoV1(BaseRepo):
    model = User

    async def create_user(
        self, data: UserInputSchema, is_admin: bool = False
    ) -> UserOutputSchema:
        """Create user"""
        obj = await self.create(**data.model_dump(), is_admin=is_admin)
        return UserOutputSchema.model_validate(obj)

    async def update_user(self, user_id: UUID, **data) -> UserOutputSchema | None:
        """Update user"""
        obj = await self.find(id=user_id)
        if not obj:
            return None
        updated_obj = await self.update(obj, **data)
        return UserOutputSchema.model_validate(updated_obj)

    async def find_user(
        self, is_password: bool = False, **filters
    ) -> UserOutputSchema | None:
        """Find user"""
        obj: User | None = await self.find(**filters, is_active=True)
        if not obj:
            return None
        user_schema = UserOutputSchema.model_validate(obj)
        if is_password:
            user_schema.password = obj.password  # type: ignore
        return user_schema

    async def delete_user(self, user_id: UUID) -> UserOutputSchema | None:
        """Deactivate user"""
        obj = await self.find(id=user_id)
        if not obj:
            return None
        if user := await self.update(obj, **{"is_active": False}):
            return UserOutputSchema.model_validate(user)
        return None
