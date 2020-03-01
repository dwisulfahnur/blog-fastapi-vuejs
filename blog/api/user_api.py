from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from blog.models import User
from blog.serializers.user import UserInSerializer, UserSerializer

router = APIRouter()


@router.get("", response_model=List[UserSerializer],
            status_code=status.HTTP_200_OK, tags=["User"])
async def get_users_api():
    cursor = User.find()
    return [user.dump() for user in await cursor.to_list(length=10)]


@router.post("", response_model=UserSerializer,
             status_code=status.HTTP_201_CREATED, tags=["User"])
async def create_user_api(user: UserInSerializer):
    user = User(email=user.email, first_name=user.first_name, last_name=user.last_name)
    try:
        created = await user.commit()
    except Exception as e:
        return JSONResponse(e.messages, status.HTTP_400_BAD_REQUEST)
    if created:
        return user.dump()
