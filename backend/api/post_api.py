from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from backend.api.auth_api import get_current_user
from backend.models.post import Post, Comment
from backend.models.user import User
from backend.serializers.comment import CommentInSerializer
from backend.serializers.post import PostInSerializer, PostSerializer

router = APIRouter()


@router.get("", response_model=List[PostSerializer],
            status_code=status.HTTP_200_OK)
async def get_posts_api():
    cursor = Post.find()
    posts = [post.dump() for post in await cursor.to_list(length=10)]
    return posts


@router.post("", response_model=PostSerializer,
             status_code=status.HTTP_201_CREATED)
async def create_post_api(post: PostInSerializer, current_user=Depends(get_current_user)):
    post = Post(title=post.title, created_by=current_user.id, content=post.content, comments=[])
    await post.commit()
    post = post.dump()
    return post


@router.get("/{post_id}", response_model=PostSerializer,
            status_code=status.HTTP_201_CREATED)
async def get_post_detail_api(post_id: str):
    post = await Post.find_one({"_id": ObjectId(post_id)})
    if post:
        return post.dump()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_api(post_id: str, current_user=Depends(get_current_user)):
    post = await Post.get(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")

    if post.created_by != current_user:
        raise HTTPException(status_code=401, detail='Not Enough Permissions')

    await post.remove()
    return


@router.post("/{post_id}/add-comment", response_model=PostSerializer,
             status_code=status.HTTP_201_CREATED)
async def add_post_comment_api(post_id: str, comment: CommentInSerializer,
                               current_user: User = Depends(get_current_user)):
    post = await Post.find_one({"_id": ObjectId(post_id)})

    if post:
        comment = Comment(created_by=current_user, content=comment.content)
        post.add_comment(comment)
        await post.commit()
        return post.dump()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post Not Found")
