from pymongo import MongoClient
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
from tenacity import retry, wait_fixed, stop_after_delay

RETRY_DELAY = 60 * 5
RETRY_INTERVAL = 3

class LogLevel(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARN = 'WARN'
    ERROR = 'ERROR'

class LogMsg(BaseModel):
    logger: str
    msg_dict: dict
    log_level: LogLevel
    updated: datetime = Field(default_factory=datetime.now)


class MongoLog(object):

    def __init__(self, mongo_uri, db, logger_name, collection="logs"):
        self.mongo_uri = mongo_uri
        self.logger_name = logger_name
        self.client = None
        self.__connect()
        self.log_collection = self.client[db][collection]

    @retry(stop=stop_after_delay(RETRY_DELAY),
           wait=wait_fixed(RETRY_INTERVAL), reraise=True)
    def __connect(self):
        print("connecting MongoDB ...")
        self.client = MongoClient(self.mongo_uri)
        self.client.server_info()
        print("MongoDB connected")

    def __disconnect(self):
        if self.client:
            self.client.close()
            print("MongoDB disconnected")

    def debug_log(self, msg_dict):
        validated_logdict = LogMsg(logger=self.logger_name, msg_dict=msg_dict, log_level="DEBUG").dict()
        self.log_collection.insert_one(validated_logdict)

    def info_log(self, msg_dict):
        validated_logdict = LogMsg(logger=self.logger_name, msg_dict=msg_dict, log_level="INFO").dict()
        self.log_collection.insert_one(validated_logdict)

    def warn_log(self, msg_dict):
        validated_logdict = LogMsg(logger=self.logger_name, msg_dict=msg_dict, log_level="WARN").dict()
        self.log_collection.insert_one(validated_logdict)

    def error_log(self, msg_dict):
        validated_logdict = LogMsg(logger=self.logger_name, msg_dict=msg_dict, log_level="ERROR").dict()
        self.log_collection.insert_one(validated_logdict)


if __name__ == "__main__":

    mongolog = MongoLog(
        mongo_uri='mongodb://root:GuardStrike!!!@dds-2zeb146fafba16441401-pub.mongodb.rds.aliyuncs.com:3717,dds-2zeb146fafba16442383-pub.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-54022070',
        db='sdgApp2',
        logger_name='sdg-logtest')

    mongolog.debug_log(msg_dict={"msg":"hello, this is a debug level message !","task_id":"123456"})
    mongolog.info_log(msg_dict={"msg":"hello, this is a info level message !","task_id":"123456"})
    mongolog.warn_log(msg_dict={"msg": "hello, this is a warn level message !", "task_id": "123456"})
    mongolog.error_log(msg_dict={"msg": "hello, this is a error level message !", "task_id": "123456"})