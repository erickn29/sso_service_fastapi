from fastapi import FastAPI

from api.router_general import router as general_router
from core.config import config


app = FastAPI(
    debug=config.app.debug,
    title="SSO",
    version="0.1.0",
    docs_url="/docs/" if config.app.debug else None,
    redoc_url="/redoc/" if config.app.debug else None,
)

app.include_router(general_router)
