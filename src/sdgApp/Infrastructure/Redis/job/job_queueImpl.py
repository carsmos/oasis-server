from walrus import Database
from sdgApp.Domain.job.job_queue import JobQueue
import json
from sdgApp.Infrastructure.MongoDB.session_maker import mongolog_session
from sdgApp.Infrastructure.conf_parser import get_conf


class JobQueueImpl(JobQueue):
    def __init__(self, sess: Database):
        self.sess = sess
        self.log = mongolog_session()

    def publish(self, queue_name: str, job: dict):
        conf = get_conf()
        queue_name = conf['DB_REDIS']['USER_ID']
        if job:
            for task in job['task_list']:
                self.sess.set(task['id'], json.dumps(task))
                self.sess.lpush(queue_name, task['id'])
                self.log.info_log({"msg": "Task in queue, waiting to be processed. task_id:{}".format(task['id']),
                                   "task_id": task['id']})
