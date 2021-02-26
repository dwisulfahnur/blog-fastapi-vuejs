from datetime import datetime, timedelta

import jwt
from bson.objectid import ObjectId
from src.core.config import SECRET_KEY, PWD_CONTEXT, ALGORITHM
from src.core.db import instance, db
from umongo import Document, fields


@instance.register
class User(Document):
    id = fields.ObjectIdField()
    full_name = fields.StrField()
    email = fields.EmailField(unique=True)
    hashed_password = fields.StrField()
    last_password_updated_at = fields.DateTimeField()
    scopes = fields.ListField(fields.StrField(), default=[])

    created_at = fields.DateTimeField(default=datetime.now)
    updated_at = fields.DateTimeField(default=datetime.now)

    class Meta:
        collection_name = 'user'
        collection = db.user

    @classmethod
    async def get(cls, id: str):
        if not ObjectId.is_valid(id):
            return None
        user = await cls.find_one({'_id': ObjectId(id)})
        return user

    @classmethod
    async def get_by_email(cls, email: str):
        return await cls.find_one({'email': email})

    def check_password(self, password: str):
        if self.hashed_password:
            return PWD_CONTEXT.verify(password, self.hashed_password)

    def set_password(self, password: str):
        self.hashed_password = PWD_CONTEXT.hash(password)
        self.last_password_updated_at = datetime.now()

    def create_access_token(self, expires_delta: timedelta = None):
        now = datetime.utcnow()
        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + timedelta(minutes=15)
        to_encode = {
            'exp': expire,
            'iat': now,
            'sub': str(self.id),
            'scope': ' '.join(self.scopes) if self.scopes else ''
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @classmethod
    async def register_new_user(cls, email: str, full_name: str, password: str):
        user = cls(email=email, full_name=full_name)
        user.set_password(password)
        await user.commit()
        return user
