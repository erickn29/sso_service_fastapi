import json
import uuid

from typing import Protocol
from uuid import UUID

from core.cache import Cache, cache_service
from core.celery import send_email_task
from core.config import config as cfg
from repository.user import UserRepoV1
from schema.user import UserInputSchema, UserOutputSchema


class UserRepoProtocol(Protocol):
    async def create_user(
        self, data: UserInputSchema, is_admin: bool = False
    ) -> UserOutputSchema:
        """Create user"""
        pass

    async def update_user(self, user_id: UUID, **data) -> UserOutputSchema | None:
        """Update user"""
        pass

    async def find_user(
        self, is_password: bool = False, **filters
    ) -> UserOutputSchema | None:
        """Find user"""
        pass

    async def delete_user(self, user_id: UUID) -> UserOutputSchema | None:
        """Deactivate user"""
        pass


class UserServiceV1:
    user_cache_key = "user:"

    def __init__(
        self, repo: type[UserRepoProtocol] = UserRepoV1, cache: Cache = cache_service
    ):
        self._repo = repo()
        self._cache = cache

    async def create(
        self, user: UserInputSchema, is_admin: bool = False
    ) -> UserOutputSchema:
        """Create user"""
        if user_obj := await self.find_by_email(email=user.email):
            return user_obj
        user.password = self.get_password_hash(user.password)
        user_obj = await self._repo.create_user(user, is_admin)
        await self._set_user_to_cache(user_obj)
        await self._send_email(user_obj)
        return user_obj

    async def update(self, user_id: UUID, **data) -> UserOutputSchema | None:
        """Update user"""
        if data.get("password"):
            data["password"] = self.get_password_hash(data["password"])
        if user := await self._repo.update_user(user_id, **data):
            await self._set_user_to_cache(user)
            return user
        return None

    async def find_by_id(self, user_id: UUID) -> UserOutputSchema | None:
        """Find user"""
        if user := await self._get_user_from_cache(user_id):
            return user
        if user := await self._repo.find_user(id=user_id):
            await self._set_user_to_cache(user)
            return user
        return None

    async def find_by_email(self, email: str) -> UserOutputSchema | None:
        """Find user"""
        if user := await self._repo.find_user(is_password=True, email=email):
            await self._set_user_to_cache(user)
            return user
        return None

    async def delete(self, user_id: UUID) -> UserOutputSchema | None:
        """Deactivate user"""
        if await self._get_user_from_cache(user_id):
            await self._cache.delete(self.user_cache_key + str(user_id))
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

    async def _set_user_to_cache(self, user: UserOutputSchema):
        user_json = UserOutputSchema.model_dump_json(user)
        await self._cache.set(
            name=self.user_cache_key + str(user.id),
            value=user_json,
            ex=cfg.auth.access_token_expire,
        )

    async def _get_user_from_cache(self, user_id: UUID) -> UserOutputSchema | None:
        if user := await self._cache.get(self.user_cache_key + str(user_id)):
            return UserOutputSchema.model_validate(json.loads(user))
        return None

    async def _send_email(self, user: UserOutputSchema):
        verification_token = str(uuid.uuid4())
        await self._cache.set(
            name=f"verification_token:{verification_token}",
            value=str(user.id),
            ex=60 * 60 * 24 * 7,
        )
        message = f"""
        Hello, {user.first_name} {user.last_name}!\n
        Please verify your email address by clicking the link below:\n
        {cfg.app.frontend_url}/verify-email?token={verification_token}
        """
        send_email_task.delay(
            email=user.email,
            subject="Registration",
            message=message,
        )

    async def verify_email(self, token: str):
        user_id: bytes = await self._cache.get(f"verification_token:{token}")
        if not user_id:
            return False
        await self._repo.update_user(UUID(user_id.decode()), is_verified=True)
        await self._cache.delete(f"verification_token:{token}")
        return True
