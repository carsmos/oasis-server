from sdgApp.Domain.job.run import Run
from sdgApp.Infrastructure.MongoDB.session_maker import mongo_log
from sdgApp.Infrastructure.Aiohttp.session_maker import SingletonAiohttp


class JobRunImpl(Run):
    def __init__(self, sess: SingletonAiohttp):
        self.sess = sess
        self.log = mongo_log.log_sess

    async def publish(self, job: dict):
        if job:
            for task in job['task_list']:
                result = await self.sess.post(param=task)
                print(result)
                self.log.info_log({"msg": "Task in queue, waiting to be processed. task_id:{}".format(task['id']),
                                   "task_id": task['id']})
