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

    def add(self, job: dict, task_ids):
        conf = get_conf()
        queue_name = conf['DB_REDIS']['USER_ID']
        task_list = job.get("task_list")

        for task_id in task_ids.split(",")[::-1]:
            add_task_list = [task for task in task_list if task_id == task.get("id")]
            if job and len(add_task_list) > 0:

                ori_idx = [task.get("id") for task in task_list].index(task_id)
                task = add_task_list[0]
                retry_task = copy.deepcopy(task)
                retry_task["original_id"] = task_id
                retry_task['result'] = ""
                retry_task["id"] = shortuuid.uuid()
                retry_task["status"] = "inqueue"
                retry_task["last_modified"] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                retry_task['replay_url'] = ""
                retry_task['cam_url'] = ""
                retry_task['process_rate'] = 0

                handle_index_for_task(task, ori_idx, task_list, retry_task)

                self.sess.set(retry_task["id"], json.dumps(retry_task))
                self.sess.rpush(queue_name, retry_task["id"])
                self.log.info_log({"msg": "Task in queue, waiting to be processed. task_id:{}".format(task_id),
                               "task_id": task_id})
        return job

    def get_length(self):
        conf = get_conf()
        queue_name = conf['DB_REDIS']['USER_ID']
        return len(self.sess.lrange(queue_name, 0, -1))


def find_parent_task(add_task, task_list):
    if add_task.get("original_id") is None:
        return add_task
    else:
        forward_task = [task for task in task_list if task.get("id") == add_task.get("original_id")]
    if len(forward_task) > 0:
        return find_parent_task(forward_task[0], task_list)


def handle_index_for_task(ori_task, ori_idx, task_list, retry_task):
    for idx, task in enumerate(task_list):
        if task.get("index") is None:
            if idx <= 9:
                task["index"] = "0" + str(idx+1)
            else:
                task["index"] = str(idx+1)
    parent_task = find_parent_task(ori_task, task_list)
    if ori_idx + 1 < len(task_list):
        for i in range(ori_idx+1, len(task_list)):
            if task_list[i].get("original_id") is None:
                if ori_idx + 1 <= 9:
                    retry_task["index"] = parent_task.get("index") + ".%s" % i
                else:
                    retry_task["index"] = parent_task.get("index") + ".%s" % i
                task_list.insert(i, retry_task)
                break
        if retry_task not in task_list:
            if ori_idx + 1 <= 9:
                retry_task["index"] = parent_task.get("index") + ".%s" % (len(task_list))
            else:
                retry_task["index"] = parent_task.get("index") + ".%s" % (len(task_list))
            task_list.insert(len(task_list), retry_task)
    else:
        parent_task_index = task_list[ori_idx].get("index")
        if "." not in parent_task_index:
            if ori_idx + 1 <= 9:
                retry_task["index"] = parent_task.get("index") + ".%s" % 1
            else:
                retry_task["index"] = parent_task.get("index") + ".%s" % 1
            task_list.insert(ori_idx + 1, retry_task)
        else:
            retry_task["index"] = parent_task_index.split(".")[0] + "." + str(int(parent_task_index.split(".")[1]) + 1)
            task_list.insert(ori_idx + 1, retry_task)

