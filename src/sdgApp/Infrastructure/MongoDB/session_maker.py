from typing import Tuple
from sdgApp.Infrastructure.conf_parser import get_conf
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Tuple
from pymongo.database import Database
from pymongo import MongoClient
from sdgApp.Infrastructure.conf_parser import get_conf
from sdgApp.Infrastructure.MongoDB.MongoLog import MongoLog

'''mongo session'''


def async_mongo_session() -> Tuple[AsyncIOMotorClient, AsyncIOMotorDatabase]:
    conf = get_conf()
    uri = conf['DB_MONGO']['MONGO_CONNECTION_STRING']
    db_name = str(conf['DB_MONGO']['MONGO_DB_NAME'])
    client = AsyncIOMotorClient(uri, uuidRepresentation="standard")
    db = client[db_name]
    return client, db


def mongo_session() -> Tuple[MongoClient, Database]:
    conf = get_conf()
    uri = conf['DB_MONGO']['MONGO_CONNECTION_STRING']
    db_name = str(conf['DB_MONGO']['MONGO_DB_NAME'])
    client = MongoClient(uri, uuidRepresentation="standard")
    db = client[db_name]
    return client, db


def mongolog_session():
    conf = get_conf()
    uri = conf['DB_MONGO']['MONGO_CONNECTION_STRING']
    db_name = str(conf['DB_MONGO']['MONGO_DB_NAME'])
    logger = "sdg-server"
    mongolog = MongoLog(mongo_uri=uri,
                        db=db_name,
                        logger_name=logger)
    return mongolog


async def get_db():
    try:
        client, db = mongo_session()
        yield db
    finally:
        client.close()
