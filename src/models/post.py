from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from umongo import Document, fields, EmbeddedDocument

from src.core.db import instance, db
from src.models.user import User


@instance.register
class Comment(EmbeddedDocument):
    id = fields.ObjectIdField(default=ObjectId())
    content = fields.StrField()

    created_by = fields.ReferenceField("User")
    created_at = fields.DateTimeField(default=datetime.now)
    updated_at = fields.DateTimeField(default=datetime.now)


@instance.register
class Post(Document):
    title = fields.StrField()
    content = fields.StrField()
    comments = fields.ListField(fields.EmbeddedField(Comment))

    author_name = fields.StrField(allow_none=True, default='')
    created_by = fields.ReferenceField(User)
    created_at = fields.DateTimeField(default=datetime.now)
    updated_at = fields.DateTimeField(default=datetime.now)

    class Meta:
        collection = db.post

    @classmethod
    async def get(cls, id: str) -> Optional['Post']:
        if not ObjectId.is_valid(id):
            return None

        return await cls.find_one({'_id': ObjectId(id)})

    def add_comment(self, comment: Comment):
        self.comments = self.comments + [comment]
