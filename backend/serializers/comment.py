from datetime import datetime

from pydantic import BaseModel


class CommentSerializer(BaseModel):
    author: str
    content: str

    created_at: datetime
    updated_at: datetime


class CommentInSerializer(BaseModel):
    author_id: str
    content: str
