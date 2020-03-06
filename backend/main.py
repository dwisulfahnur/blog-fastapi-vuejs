import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from backend.api import router
from .core import config
from .core.db import database

app = FastAPI(title="Blog API")

origins= [
    'http://localhost:8000',
    'http://localhost:8080'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event("startup")
async def event_startup():
    logging.info("connect to database....")
    database.client = AsyncIOMotorClient(str(config.MONGODB_URI))
    logging.info("Connected to database!")

    logging.info("ensuring model indexes")
    from backend.models import ensure_indexes
    await ensure_indexes()


@app.on_event("shutdown")
async def event_shutdown():
    logging.info("close mongodb connection....")
    database.client.close()
    logging.info("connection to mongodb has been closed!")


app.include_router(router, prefix="/api")
