from datetime import datetime

from umongo import Document, fields, EmbeddedDocument

from backend.core.db import instance, db
from backend.models.user import User
from bson.objectid import ObjectId

@instance.register
class Comment(EmbeddedDocument):
    id = fields.ObjectIdField(default=ObjectId())
    content = fields.StrField()

    created_by = fields.ReferenceField("User")
    created_at = fields.DateTimeField(default=datetime.now())
    updated_at = fields.DateTimeField(default=datetime.now())


@instance.register
class Post(Document):
    title = fields.StrField()
    content = fields.StrField()
    comments = fields.ListField(fields.EmbeddedField(Comment))

    created_by = fields.ReferenceField(User)
    created_at = fields.DateTimeField(default=datetime.now())
    updated_at = fields.DateTimeField(default=datetime.now())

    class Meta:
        collection = db.post

    @classmethod
    async def get(cls, id:str):
        if not ObjectId.is_valid(id):
            return None

        return await cls.find_one({'_id': ObjectId(id)})

    def add_comment(self, comment: Comment):
        self.comments = self.comments + [comment]
