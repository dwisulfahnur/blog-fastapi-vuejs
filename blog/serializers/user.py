from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSerializer(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: Optional[str]

    created_at: datetime
    updated_at: datetime


class UserInSerializer(BaseModel):
    email: EmailStr
    first_name: str
    last_name: Optional[str]
