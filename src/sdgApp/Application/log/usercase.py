from sdgApp.Infrastructure.MongoDB.log.log_repoImpl import LogRepoImpl
from sdgApp.Domain.log.log import LogAggregate

from utils.logger_utils import LogWrapper
from functools import wraps
import traceback

loggerd = LogWrapper(server_name="oasis-server").getlogger()

def except_logger(msg='exception'):
    def except_execute(func):
        @wraps(func)
        async def execept_print(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                loggerd.error(msg)
                loggerd.error(traceback.format_exc())
                raise

        return execept_print

    return except_execute

def dto_assembler(log: LogAggregate):
    return log.shortcut_DO

class LogQueryUsercase(object):

    def __init__(self, db_session, repo=LogRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session)

    @except_logger("list_log failed .....................")
    async def list_log(self, task_id:str, level:str):
        try:
            response_dto_lst = []
            log_lst = await self.repo.list(task_id, level)
            if log_lst:
                for log in log_lst:
                    response_dto = dto_assembler(log)
                    response_dto_lst.append(response_dto)
                return response_dto_lst
        except:
            raise