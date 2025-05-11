from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware import Middleware

from api.router_general import router as general_router
from core.config import config
from core.log import logger
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

Instrumentator().instrument(app).expose(app)


@app.get("/")
async def root():
    import random

    number = random.randint(0, 2)
    if number == 0:
        return {"message": "Hello World"}
    if number == 1:
        logger.error("Bad Request")
        raise HTTPException(400, "Bad Request")
    if number == 2:
        logger.error("Internal Server Error")
        raise HTTPException(500, "Internal Server Error")
    return {"message": "Hello World"}
