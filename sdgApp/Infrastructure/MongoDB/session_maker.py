from typing import Tuple
from sdgApp.Infrastructure.conf_parser import get_conf
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Tuple
from pymongo.database import Database
from pymongo import MongoClient
from sdgApp.Infrastructure.conf_parser import get_conf

'''mongo session'''


def async_mongo_session() -> Tuple[AsyncIOMotorClient, AsyncIOMotorDatabase]:
    conf = get_conf()
    uri = conf['DB Mongo']['connection_string']
    db_name = str(conf['DB Mongo']['db_name'])
    client = AsyncIOMotorClient(uri, uuidRepresentation="standard")
    db = client[db_name]
    return client, db

def mongo_session() -> Tuple[MongoClient, Database]:
    conf = get_conf()
    uri = conf['DB Mongo']['connection_string']
    db_name = str(conf['DB Mongo']['db_name'])
    client = MongoClient(uri, uuidRepresentation="standard")
    db = client[db_name]
    return client, db

