from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from src.api.auth_api import get_current_user
from src.models.post import Post, Comment
from src.models.user import User
from src.serializers.comment import CommentInSerializer
from src.serializers.post import PostInSerializer, PostSerializer, PostInPatchSerializer

router = APIRouter()


def pagination(skip: int = 0, limit: int = 10):
    return {
        'skip': skip,
        'limit': limit
    }


@router.get("", response_model=List[PostSerializer],
            status_code=status.HTTP_200_OK)
async def get_posts_api(pagination=Depends(pagination)):
    cursor = Post.find() \
        .sort('created_at', -1) \
        .skip(pagination['skip']) \
        .limit(pagination['limit'])

    posts = [post.dump() for post in await cursor.to_list(length=pagination['limit'])]
    return posts


@router.get("/me", response_model=List[PostSerializer])
async def get_my_posts_api(pagination=Depends(pagination), current_user=Depends(get_current_user)):
    cursor = Post.find({'created_by': current_user.id}) \
        .sort('created_at', -1) \
        .skip(pagination['skip']) \
        .limit(pagination['limit'])

    posts = [post.dump() for post in await cursor.to_list(length=pagination['limit'])]
    return posts


@router.post("", response_model=PostSerializer,
             status_code=status.HTTP_201_CREATED)
async def create_post_api(post: PostInSerializer, current_user:User=Depends(get_current_user)):
    post = Post(
        title=post.title,
        created_by=current_user.id,
        content=post.content,
        comments=[],
        author_name=current_user.full_name
    )

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


@router.patch("/{post_id}", response_model=PostSerializer, status_code=status.HTTP_200_OK)
async def update_post_api(post_id: str, post_in: PostInPatchSerializer, current_user=Depends(get_current_user)):
    post = await Post.get(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")

    if post.created_by != current_user:
        raise HTTPException(status_code=401, detail='Not Enough Permissions')

    if post_in.title:
        post.title = post_in.title
    if post_in.content:
        post.content = post_in.content

    post.updated_at = datetime.now()
    await post.commit()
    return post.dump()


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
