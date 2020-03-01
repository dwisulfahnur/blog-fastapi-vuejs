from fastapi import APIRouter

from .post_api import router as post_router
from .user_api import router as user_router

router = APIRouter()

router.include_router(prefix="/posts", router=post_router)
router.include_router(prefix="/users", router=user_router)
