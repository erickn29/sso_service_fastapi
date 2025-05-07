from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


async def get_http_client(
    app: FastAPI,
    base_url: str = "http://127.0.0.1:1234",
    cookies: dict[str, str] = None,
    headers: dict[str, str] = None,
) -> AsyncClient:
    return AsyncClient(
        transport=ASGITransport(app=app),
        base_url=base_url,
        cookies=cookies,
        headers=headers,
    )
