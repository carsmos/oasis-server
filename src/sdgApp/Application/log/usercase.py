from sdgApp.Infrastructure.MongoDB.log.log_repoImpl import LogRepoImpl
from sdgApp.Domain.log.log import LogAggregate

def dto_assembler(log: LogAggregate):
    return log.shortcut_DO

class LogQueryUsercase(object):

    def __init__(self, db_session, repo=LogRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session)

    def get_log(self, task_id:str, level:str):
        try:
            log = self.repo.get(task_id, level)
            if log:
                response_dto = dto_assembler(log)
                return response_dto
        except:
            raise