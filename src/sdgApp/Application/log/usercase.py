from sdgApp.Infrastructure.MongoDB.log.log_repoImpl import LogRepoImpl
from sdgApp.Domain.log.log import LogAggregate

def dto_assembler(log: LogAggregate):
    return log.shortcut_DO

class LogQueryUsercase(object):

    def __init__(self, db_session, repo=LogRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session)

    def list_log(self, task_id:str, level:str):
        try:
            response_dto_lst = []
            log_lst = self.repo.list(task_id, level)
            if log_lst:
                for log in log_lst:
                    response_dto = dto_assembler(log)
                    response_dto_lst.append(response_dto)
                return response_dto_lst
        except:
            raise