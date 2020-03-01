from datetime import datetime
from typing import List

from pydantic import BaseModel

from .comment import CommentSerializer


class PostSerializer(BaseModel):
    id: str
    title: str
    author: str
    content: str
    comments: List[CommentSerializer] = []

    created_at: datetime
    updated_at: datetime


class PostInSerializer(BaseModel):
    title: str
    author_id: str
    content: str

    # @validator("author_id")
    # def validate_author_id(cls, v):
    #     if v:
    #         user = asyncio.get_running_loop(User.find_one({"_id": v}))
    #         user = asyncio.ensure_future(user)
    #         print("================")
    #         print(user.result())
    #         if user:
    #             return v
    #     raise ValueError("author_id is not valid")
