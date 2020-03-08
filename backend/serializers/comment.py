from datetime import datetime

from pydantic import BaseModel


class CommentSerializer(BaseModel):
    id: str
    content: str

    created_by: str
    created_at: datetime
    updated_at: datetime


class CommentInSerializer(BaseModel):
    content: str
