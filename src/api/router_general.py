from fastapi import APIRouter, Depends

from api.v1.router_v1 import router as router_v1
from deps.auth import is_admin_or_service


router = APIRouter(prefix="/api", dependencies=[Depends(is_admin_or_service)])

router.include_router(router_v1)


@router.get("/healthcheck/", status_code=200)
async def health_check():
    return {"status": "ok"}
