from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Instance

from backend.core import config


class DataBase:
    client: AsyncIOMotorClient = None


database = DataBase()


def get_database():
    if database.client:
        return database.client[config.database_name]
    return AsyncIOMotorClient(config.MONGODB_URI)[config.database_name]


def get_client():
    if not database.client:
        return AsyncIOMotorClient(config.MONGODB_URI)
    return database.client


db = get_database()
instance = Instance(db)
