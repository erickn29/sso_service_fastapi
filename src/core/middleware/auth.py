from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    BaseUser,
    UnauthenticatedUser,
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.types import Receive, Scope, Send


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


class SSOAuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, BaseUser] | None:
        token = (
            conn.cookies.get("access_token")
            or conn.headers.get("Authorization")
            or conn.headers.get("x-auth-token")
        )
        if not token:
            raise AuthenticationError("Токен не был предоставлен")
        return None
