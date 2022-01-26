from sdgApp.Domain.job.task import TaskEntity

class JobAggregate(object):

    def __init__(self, id,
                 name=None,
                 desc=None):
        self.id = id
        self.name = name
        self.desc = desc
        self.task_list = []

    def add_task(self, task: TaskEntity):
        task.attach_to(self.id)
        task_dict = {"id":task.id,
                     "name":task.name ,
                     "desc":task.desc,
                     "car_id":task.car_id,
                     "car_name":task.car_name,
                     "scenario_id":task.scenario_id,
                     "scenario_name":task.scenario_name,
                     "result":task.result,
                     "job_id":task.job_id,
                     "status":task.status,
                     "replay_url":task.replay_url}
        self.task_list.append(task_dict)

    def save_DO_shortcut(self, DO:dict):
        self.shortcut_DO = DO

