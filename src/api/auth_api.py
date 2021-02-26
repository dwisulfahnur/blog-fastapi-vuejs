from datetime import timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.core.config import ACCESS_TOKEN_EXPIRES, SECRET_KEY, ALGORITHM
from src.models.user import User
from src.serializers.token import Token, TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/oauth/token')
router = APIRouter()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception
        token_data = TokenData(sub=sub)
    except jwt.PyJWTError:
        raise credentials_exception
    user = await User.get(token_data.sub)
    if user is None:
        raise credentials_exception
    return user


@router.post('/token', response_model=Token)
async def get_token_api(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_by_email(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not user.check_password(form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = user.create_access_token(expires_delta=timedelta(hours=ACCESS_TOKEN_EXPIRES))
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/tokeninfo', status_code=status.HTTP_200_OK)
async def get_token_info_api(token: str = None):
    credentials_exception = HTTPException(
        detail='Token is not valid',
        status_code=status.HTTP_401_UNAUTHORIZED)
    if not token: raise credentials_exception
    try:
        payload = jwt.decode(token.encode(), SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        if sub is None or not await User.get(sub):
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return payload
