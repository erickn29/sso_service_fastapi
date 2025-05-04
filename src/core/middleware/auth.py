import json

from datetime import datetime
from uuid import UUID

import jwt

from jwt import InvalidTokenError
from starlette.authentication import (
    AuthCredentials,
    AuthenticationError,
    UnauthenticatedUser,
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.types import Receive, Scope, Send

from core.cache import cache_service
from core.config import config
from core.constants import TZ
from schema.user import UserOutputSchema
from service.user import UserServiceV1


class SSOAuthMiddleware(AuthenticationMiddleware):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope)
        if not any(
            map(
                lambda x: x in conn.url.path,
                ["/docs", "/redoc", "/openapi.json"],
            )
        ):
            try:
                auth_result = await self.backend.authenticate(conn)
            except AuthenticationError as exc:
                response = self.on_error(conn, exc)
                if scope["type"] == "websocket":
                    await send({"type": "websocket.close", "code": 1000})
                else:
                    await response(scope, receive, send)
                return

            if auth_result is None:
                auth_result = AuthCredentials(), UnauthenticatedUser()
            scope["auth"], scope["user"] = auth_result
        await self.app(scope, receive, send)


class SSOAuthBackend:
    user_cache_key = "user:"
    token_expires_in = 60 * 5

    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, UserOutputSchema] | None:
        if token := conn.cookies.get("access_token"):  # noqa SIM102
            if user := await self._get_user(token):
                return AuthCredentials(["authenticated"]), user

        if token := conn.headers.get("x-api-key"):  # noqa SIM102
            if user := await self._get_service(token):
                return AuthCredentials(["authenticated"]), user

        return None

    async def _get_user(self, token: str) -> UserOutputSchema | None:
        token_data = self._get_token_payload(token)
        self._check_iat(token_data)
        user_id = token_data.get("id")
        if not user_id:
            return None
        user_id = self._validate_token(user_id)
        if not user_id:
            return None
        return await self._find_user(user_id)

    async def _get_service(self, token: str) -> UserOutputSchema | None:
        service_id = self._validate_token(token)
        if not service_id:
            return None
        return await self._find_user(service_id)

    async def _find_user(self, user_id: UUID):
        if user := await cache_service.get(self.user_cache_key + str(user_id)):
            return UserOutputSchema.model_validate(json.loads(user))
        user_service = UserServiceV1()
        if user := await user_service.find(user_id=user_id):
            user_json = UserOutputSchema.model_dump_json(user)
            await cache_service.set(
                name=self.user_cache_key + str(user_id),
                value=user_json,
                expires_in=self.token_expires_in,
            )
            return user
        return None

    @staticmethod
    def _validate_token(token: str) -> UUID | None:
        if not token:
            return None
        try:
            token_uuid = UUID(token)
            return token_uuid
        except ValueError:
            return None

    @staticmethod
    def _get_token_payload(token: str) -> dict:
        try:
            return jwt.decode(
                jwt=token, verify=True, algorithms="HS256", key=config.app.secret_key
            )
        except InvalidTokenError as e:
            raise AuthenticationError("Ошибка получения token payload") from e

    @staticmethod
    def _check_iat(payload: dict):
        if not payload or not payload.get("expat"):
            raise AuthenticationError("Не найден expat expat")
        try:
            expat = float(payload.get("expat", 0))
        except ValueError:
            raise AuthenticationError("Неверный формат даты в jwt") from None
        if datetime.now(tz=TZ.MSK).timestamp() > expat:
            raise AuthenticationError("Обновите токен")
