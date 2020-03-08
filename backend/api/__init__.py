from fastapi import APIRouter

from .auth_api import router as oauth_router
from .post_api import router as post_router
from .user_api import router as user_router

router = APIRouter()

router.include_router(prefix="/oauth", router=oauth_router, tags=['OAuth2'])
router.include_router(prefix="/users", router=user_router, tags=['Users'])
router.include_router(prefix="/posts", router=post_router, tags=['Posts'])
