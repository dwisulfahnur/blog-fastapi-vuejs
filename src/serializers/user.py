from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class UserSerializer(BaseModel):
    id: str
    full_name: Optional[str]
    email: EmailStr

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserInSerializer(BaseModel):
    full_name: str
    email: EmailStr
    password: str

    @validator('full_name')
    def validate_full_name(cls, v):
        if not v:
            raise ValueError('Full Name is required')
        return v

    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password is required to create a new account')
        if v and len(v) < 8:
            raise ValueError('Password must be more than 8 characters')
        return v
