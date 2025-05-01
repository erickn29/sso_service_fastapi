from typing import Protocol
from uuid import UUID

from core.config import config as cfg
from repository.user import UserRepoV1
from schema.user import UserInputSchema, UserOutputSchema


class UserRepoProtocol(Protocol):
    async def create_user(self, data: UserInputSchema) -> UserOutputSchema:
        """Create user"""
        pass

    async def update_user(self, user_id: UUID, **data) -> UserOutputSchema | None:
        """Update user"""
        pass

    async def find_user(self, user_id: UUID) -> UserOutputSchema | None:
        """Find user"""
        pass

    async def delete_user(self, user_id: UUID):
        """Deactivate user"""
        pass


class UserServiceV1:
    def __init__(self, repo: type[UserRepoProtocol] = UserRepoV1):
        self._repo = repo()

    async def create(self, user: UserInputSchema) -> UserOutputSchema:
        """Create user"""
        hashed_password = self.get_password_hash(user.password)
        user.password = hashed_password
        return await self._repo.create_user(user)

    async def update(self, user_id: UUID, **data) -> UserOutputSchema | None:
        """Update user"""
        return await self._repo.update_user(user_id, **data)

    async def find(self, user_id: UUID) -> UserOutputSchema | None:
        """Find user"""
        return await self._repo.find_user(user_id)

    async def delete(self, user_id: UUID):
        """Deactivate user"""
        return await self._repo.delete_user(user_id)

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        """Сравнивает пароль в БД и из формы, True если соль и пароль верные"""
        return cfg.auth.pwd_context.verify(
            cfg.app.secret_key + plain_password, hashed_password
        )

    @staticmethod
    def get_password_hash(password) -> str:
        """Хэширует пароль пользователя, нужно для регистрации или смены пароля"""
        return cfg.auth.pwd_context.hash(cfg.app.secret_key + password)
