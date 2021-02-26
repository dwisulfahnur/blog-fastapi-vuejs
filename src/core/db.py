from src.core import config
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from umongo.frameworks import MotorAsyncIOInstance


class DataBase:
    client: AsyncIOMotorClient = None


database = DataBase()


def get_database() -> AsyncIOMotorDatabase:
    if database.client:
        return database.client[config.database_name]
    return AsyncIOMotorClient(config.MONGODB_URI)[config.database_name]


def get_client() -> AsyncIOMotorClient:
    if not database.client:
        return AsyncIOMotorClient(config.MONGODB_URI)
    return database.client


db = get_database()
instance = MotorAsyncIOInstance(db)
