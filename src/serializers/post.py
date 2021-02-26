from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .comment import CommentSerializer


class PostSerializer(BaseModel):
    id: str
    title: str
    content: str
    comments: List[CommentSerializer] = []

    created_by: str
    created_at: datetime
    updated_at: datetime


class PostInSerializer(BaseModel):
    title: str
    content: str


class PostInPatchSerializer(BaseModel):
    title: Optional[str]
    content: Optional[str]
