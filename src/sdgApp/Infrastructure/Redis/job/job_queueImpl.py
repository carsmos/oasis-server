from walrus import Database
from sdgApp.Domain.job.job_queue import JobQueue
from sdgApp.Domain.job.job import JobAggregate
import json
from sdgApp.Infrastructure.MongoDB.session_maker import mongolog_session

class JobQueueImpl(JobQueue):
    def __init__(self, sess: Database):
        self.sess = sess
        self.log = mongolog_session()

    def publish(self, queue_name: str, job: JobAggregate):
        job_DO = job.shortcut_DO
        if job_DO:
            for task_DO in job_DO['task_list']:
                self.sess.set(task_DO['id'], json.dumps(task_DO))
                self.sess.lpush(queue_name, task_DO['id'])
                self.log.info_log({"msg":"Task in queue, waiting to be processed. task_id:{}".format(task_DO['id']),
                                   "task_id": task_DO['id']})