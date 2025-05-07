from datetime import datetime
from typing import Protocol
from uuid import UUID

import jwt

from fastapi import HTTPException
from jwt import InvalidTokenError

from core.cache import Cache, cache_service
from core.config import config
from core.constants import TZ
from schema.auth import LoginSchema
from schema.user import UserInputSchema, UserOutputSchema
from service.user import UserServiceV1


class UserServiceProtocol(Protocol):
    def __init__(self, cache: Cache = cache_service):
        """Init"""
        pass

    async def create(
        self, user: UserInputSchema, is_admin: bool = False
    ) -> UserOutputSchema:
        """Create user"""
        pass

    async def update(self, user_id: UUID, **data) -> UserOutputSchema | None:
        """Update user"""
        pass

    async def find_by_id(self, user_id: UUID) -> UserOutputSchema | None:
        """Find user"""
        pass

    async def find_by_email(self, email: str) -> UserOutputSchema | None:
        """Find user"""
        pass

    async def delete(self, user_id: UUID) -> UserOutputSchema | None:
        """Deactivate user"""
        pass

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        """Сравнивает пароль в БД и из формы, True если соль и пароль верные"""
        pass

    @staticmethod
    def get_password_hash(password) -> str:
        """Хэширует пароль пользователя, нужно для регистрации или смены пароля"""
        pass


class AuthService:
    def __init__(
        self,
        user_service: type[UserServiceProtocol] = UserServiceV1,
        cache: Cache = cache_service,
    ):
        self._cache = cache
        self._user_service = user_service(cache=self._cache)

    async def get_tokens(self, login_data: LoginSchema) -> dict[str, str] | None:
        """Get refresh and access tokens to user"""
        user = await self._user_service.find_by_email(login_data.email)
        if not user:
            return None
        if not hasattr(user, "password"):
            return None
        if not self._user_service.verify_password(login_data.password, user.password):  # type: ignore
            return None
        refresh_token = self._get_token(str(user.id), config.auth.refresh_token_expire)
        access_token = self._get_token(str(user.id), config.auth.access_token_expire)
        return {"refresh_token": refresh_token, "access_token": access_token}

    @staticmethod
    def _get_token(user_id: str, exp_time: int):
        now = datetime.now(tz=TZ.MSK).timestamp()
        return jwt.encode(
            {"id": str(user_id), "expat": now + exp_time},
            config.app.secret_key,
            "HS256",
        )

    def refresh_access_token(self, refresh_token: str) -> str:
        """Refresh access token"""
        payload = self.get_payload(refresh_token)
        if not payload:
            raise HTTPException(400, "Ошибка получения payload")
        self._check_expat(payload)
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(400, "Не найден user id")
        return self._get_token(user_id, config.auth.access_token_expire)

    def verify_token(self, token: str) -> bool:
        """Check payload and token expires time"""
        payload = self.get_payload(token)
        if not payload:
            return False
        try:
            self._check_expat(payload)
        except (HTTPException, ValueError):
            return False
        return True

    @staticmethod
    def get_payload(token: str) -> dict[str, str] | None:
        try:
            return jwt.decode(
                jwt=token, verify=True, algorithms="HS256", key=config.app.secret_key
            )
        except InvalidTokenError:
            return None

    @staticmethod
    def _check_expat(payload: dict | None):
        if not payload or not payload.get("expat"):
            raise HTTPException(400, "Не найден expat")
        try:
            expat = float(payload.get("expat", 0))
        except ValueError:
            raise HTTPException(400, "Неверный формат даты в jwt") from None
        if datetime.now(tz=TZ.MSK).timestamp() > expat:
            raise HTTPException(400, "Обновите токен")
