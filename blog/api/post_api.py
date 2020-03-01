from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException
from starlette import status

from blog.models import Post, User, Comment
from blog.serializers.comment import CommentInSerializer
from blog.serializers.post import PostInSerializer, PostSerializer

router = APIRouter()


@router.get("", response_model=List[PostSerializer],
            status_code=status.HTTP_200_OK, tags=["Post"])
async def get_posts_api():
    cursor = Post.find()
    posts = [post.dump() for post in await cursor.to_list(length=10)]
    return posts


@router.post("", response_model=PostSerializer,
             status_code=status.HTTP_201_CREATED, tags=["Post"])
async def create_post_api(post: PostInSerializer):
    user = await User.find_one({"_id": ObjectId(post.author_id)})
    if user:
        post = Post(title=post.title, author=user.id, content=post.content, comments=[])
        await post.commit()
        post = post.dump()
        return post
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="author_id is not valid")


@router.get("/{post_id}", response_model=PostSerializer,
            status_code=status.HTTP_201_CREATED, tags=["Post"])
async def get_post_detail_api(post_id: str, post: PostInSerializer):
    post = await Post.find_one({"_id": ObjectId(post_id)})
    if post:
        return post.dump()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")


@router.post("/{post_id}/add-comment", response_model=PostSerializer,
             status_code=status.HTTP_201_CREATED, tags=["Post"])
async def add_post_comment_api(post_id: str, comment: CommentInSerializer):
    post = await Post.find_one({"_id": ObjectId(post_id)})
    user = await User.find_one({"_id": ObjectId(comment.author_id)})

    if post and user:
        comment = Comment(author=ObjectId(comment.author_id), content=comment.content)
        post.add_comment(comment)
        await post.commit()
        return post.dump()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="author_id is not valid")
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post Not Found")
