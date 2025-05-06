from fastapi import APIRouter

from api.v1.auth.controller import router as auth_router
from api.v1.user.controller import router as user_router


router = APIRouter(prefix="/v1")

router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(user_router, prefix="/user", tags=["Users"])
