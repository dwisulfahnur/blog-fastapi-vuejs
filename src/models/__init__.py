from .post import Post
from .user import User


async def ensure_indexes():
    await User.ensure_indexes()
    await Post.ensure_indexes()
