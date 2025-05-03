from typing import Annotated

from fastapi import APIRouter, Depends

from api.v1.router_v1 import router as router_v1
from deps.auth import is_service
from schema.user import UserOutputSchema


router = APIRouter(prefix="")

router.include_router(router_v1)


@router.get("/healthcheck", status_code=200)
async def health_check(service: Annotated[UserOutputSchema, Depends(is_service)]):
    return {"status": "ok", "service": str(service.id)}
