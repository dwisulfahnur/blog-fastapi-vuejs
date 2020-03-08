from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class UserSerializer(BaseModel):
    id: str
    full_name: Optional[str]
    email: EmailStr
    username: str

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserInSerializer(BaseModel):
    full_name: Optional[str]
    email: EmailStr
    username: str
    password: str

    @validator('password')
    def validate_password(cls, v):
        if v and len(v) < 8:
            raise ValueError('Password must be more than 8 characters')
        return v
