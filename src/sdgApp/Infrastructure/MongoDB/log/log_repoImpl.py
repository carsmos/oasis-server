from sdgApp.Domain.log.log_repo import LogRepo
from sdgApp.Domain.log.log import LogAggregate

class LogRepoImpl(LogRepo):

    def __init__(self, db_session):
        self.db_session = db_session
        self.log_collection = self.db_session['logs']

    def get(self, task_id: str, level: str):
        if level == "DEBUG":
            filter = {"msg_dict.task_id": task_id}

        elif level == "INFO":
            filter = {"$and":[{"msg_dict.task_id": task_id, "log_level":"INFO"},
                              {"msg_dict.task_id": task_id, "log_level":"WARN"},
                              {"msg_dict.task_id": task_id, "log_level": "ERROR"}]}

        elif level == "WARN":
            filter = {"$and": [{"msg_dict.task_id": task_id, "log_level": "WARN"},
                               {"msg_dict.task_id": task_id, "log_level": "ERROR"}]}

        elif level == "ERROR":
            filter = {"msg_dict.task_id": task_id, "log_level":"ERROR"}

        results_DO = self.log_collection.find(filter, {'_id': 0}).sort({"updated": 1})
