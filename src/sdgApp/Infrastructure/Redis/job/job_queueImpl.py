import copy
import datetime

import shortuuid
from walrus import Database
from sdgApp.Domain.job.job_queue import JobQueue
import json

from sdgApp.Domain.job.task import TaskEntity
from sdgApp.Infrastructure.MongoDB.session_maker import mongo_log
from sdgApp.Infrastructure.conf_parser import get_conf


class JobQueueImpl(JobQueue):
    def __init__(self, sess: Database):
        self.sess = sess
        self.log = mongo_log.log_sess

    def publish(self, job: dict):
        conf = get_conf()
        queue_name = conf['DB_REDIS']['USER_ID']
        if job:
            for task in job['task_list']:
                self.sess.set(task['id'], json.dumps(task))
                self.sess.lpush(queue_name, task['id'])
                self.log.info_log({"msg": "Task in queue, waiting to be processed. task_id:{}".format(task['id']),
                                   "task_id": task['id']})

    def delete(self, job: dict):
        conf = get_conf()
        queue_name = conf['DB_REDIS']['USER_ID']
        if job:
            for task in job['task_list']:
                self.sess.delete(task['id'])
                self.sess.lrem(queue_name, 0, task['id'])
            self.log.info_log({"msg": "Job id={} has stopped".format(job.get('id'))})

    def add(self, job: dict, task_id):
        conf = get_conf()
        queue_name = conf['DB_REDIS']['USER_ID']
        add_task_list = [task for task in job.get("task_list") if task_id == task.get("id")]
        if job and len(add_task_list) > 0:
            task = add_task_list[0]
            retry_task = copy.deepcopy(task)
            retry_task["original_id"] = task_id
            retry_task["id"] = shortuuid.uuid()
            retry_task["status"] = "inqueue"
            retry_task["last_modified"] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            job.get("task_list").append(retry_task)
            self.sess.set(task_id, json.dumps(task))
            self.sess.lpush(queue_name, task_id)
            self.log.info_log({"msg": "Task in queue, waiting to be processed. task_id:{}".format(task_id),
                           "task_id": task_id})
        return job

    def get_length(self, queue_name="sdg"):
        return len(self.sess.lrange(queue_name, 0, -1))