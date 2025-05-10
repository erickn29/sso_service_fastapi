from fastapi import FastAPI
from starlette.middleware import Middleware
from core.config import config
from api.router_general import router as general_router

from core.middleware.auth import SSOAuthBackend, SSOAuthMiddleware


middleware = [
    Middleware(SSOAuthMiddleware, backend=SSOAuthBackend()),
]


app = FastAPI(
    debug=config.app.debug,
    title="SSO",
    version="0.1.0",
    docs_url="/docs/" if config.app.debug else None,
    redoc_url="/redoc/" if config.app.debug else None,
    middleware=middleware,
)

app.include_router(general_router)
