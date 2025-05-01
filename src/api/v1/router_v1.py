from fastapi import APIRouter
from api.v1.token.controller import router as token_router
from api.v1.user.controller import router as user_router


router = APIRouter(prefix="/v1")

router.include_router(token_router)
router.include_router(user_router)
