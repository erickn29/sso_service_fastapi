from fastapi import APIRouter

from api.v1.router_v1 import router as router_v1


router = APIRouter(prefix="")

router.include_router(router_v1)
