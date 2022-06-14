from typing import Tuple
from sdgApp.Infrastructure.conf_parser import get_conf
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Tuple
from pymongo import MongoClient
from sdgApp.Infrastructure.conf_parser import get_conf
from sdgApp.Infrastructure.MongoDB.MongoLog import MongoLog
from sdgApp.Application.log.usercase import loggerd,except_logger

'''mongo log'''
class Database_log:
    log_sess: None

mongo_log = Database_log()

def mongolog_connect():
    conf = get_conf()
    uri = conf['DB_MONGO']['MONGO_CONNECTION_STRING']
    db_name = str(conf['DB_MONGO']['MONGO_DB_NAME'])
    logger = "sdg-server"
    mongolog = MongoLog(mongo_uri=uri,
                        db=db_name,
                        logger_name=logger)
    mongo_log.log_sess = mongolog
    loggerd.info("Mongo Log initialized")


'''mongo session'''

class Database:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

mongo_db = Database()

async def get_db():
    return mongo_db.db

def database_connect():
    conf = get_conf()
    uri = conf['DB_MONGO']['MONGO_CONNECTION_STRING']
    db_name = str(conf['DB_MONGO']['MONGO_DB_NAME'])
    mongo_db.client = AsyncIOMotorClient(uri, uuidRepresentation="standard")
    mongo_db.db = mongo_db.client[db_name]
    loggerd.info("MongoDB connected")

def close():
    mongo_db.client.close()
    loggerd.info("mongoDB disconnected")
