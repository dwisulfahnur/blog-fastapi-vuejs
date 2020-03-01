from datetime import datetime

from umongo import Document, fields, Instance, EmbeddedDocument

from blog.core.db import get_database

db = get_database()
instance = Instance(db)


@instance.register
class User(Document):
    email = fields.EmailField(unique=True)
    first_name = fields.StrField()
    last_name = fields.StrField()

    created_at = fields.DateTimeField(default=datetime.now())
    updated_at = fields.DateTimeField(default=datetime.now())

    class Meta:
        collection = db.user


@instance.register
class Comment(EmbeddedDocument):
    author = fields.ReferenceField("User")
    content = fields.StrField()

    created_at = fields.DateTimeField(default=datetime.now())
    updated_at = fields.DateTimeField(default=datetime.now())


@instance.register
class Post(Document):
    title = fields.StrField()
    author = fields.ReferenceField(User)
    content = fields.StrField()
    comments = fields.ListField(fields.EmbeddedField(Comment))

    created_at = fields.DateTimeField(default=datetime.now())
    updated_at = fields.DateTimeField(default=datetime.now())

    class Meta:
        collection = db.post

    def add_comment(self, comment: Comment):
        self.comments = self.comments + [comment]


async def ensure_indexes():
    await User.ensure_indexes()
    await Post.ensure_indexes()