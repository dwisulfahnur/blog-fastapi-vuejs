from motor.motor_asyncio import AsyncIOMotorClient

from backend.core import config

class DataBase:
    client: AsyncIOMotorClient = None


database = DataBase()


def get_database():
    if database.client:
        return database.client[config.database_name]
    return AsyncIOMotorClient(config.MONGODB_URI)[config.database_name]
