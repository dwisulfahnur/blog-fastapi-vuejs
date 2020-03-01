import logging

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from blog.api import router
from .core import config
from .core.db import database

app = FastAPI(title="Blog API")


@app.on_event("startup")
async def event_startup():
    logging.info("connect to database....")
    database.client = AsyncIOMotorClient(str(config.MONGODB_URI))
    logging.info("Connected to database!")

    logging.info("ensuring model indexes")
    from blog.models import ensure_indexes
    await ensure_indexes()


@app.on_event("shutdown")
async def event_shutdown():
    logging.info("close mongodb connection....")
    database.client.close()
    logging.info("connection to mongodb has been closed!")


app.include_router(router, prefix="/api")
