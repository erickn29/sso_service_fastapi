from datetime import datetime
from uuid import UUID

from starlette.authentication import (
    AuthCredentials,
    AuthenticationError,
    UnauthenticatedUser,
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.types import Receive, Scope, Send

from core.constants import TZ
from schema.user import UserOutputSchema
from service.auth import AuthService
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

    @staticmethod
    async def _find_user(user_id: UUID) -> UserOutputSchema | None:
        return await UserServiceV1().find_by_id(user_id=user_id)

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
        if payload := AuthService().get_payload(token):
            return payload
        raise AuthenticationError("Error decode token")

    @staticmethod
    def _check_iat(payload: dict):
        if not payload or not payload.get("expat"):
            raise AuthenticationError("Expat not found")
        try:
            expat = float(payload.get("expat", 0))
        except ValueError:
            raise AuthenticationError("Bad date format (need timestamp)") from None
        if datetime.now(tz=TZ.MSK).timestamp() > expat:
            raise AuthenticationError("Please, refresh token")
