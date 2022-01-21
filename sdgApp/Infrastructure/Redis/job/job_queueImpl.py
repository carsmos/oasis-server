from walrus import Database
from sdgApp.Domain.job.job_queue import JobQueue
from sdgApp.Domain.job.job import JobAggregate
import json

class JobQueueImpl(JobQueue):
    def __init__(self, sess: Database):
        self.sess = sess

    def publish(self, queue_name: str, job: JobAggregate):
        job_DO = job.shortcut_DO
        if job_DO:
            for task_DO in job_DO['task_list']:
                self.sess.set(task_DO['id'], json.dumps(task_DO))
                self.sess.lpush(queue_name, task_DO['id'])