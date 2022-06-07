from sdgApp.Domain.job.task import TaskEntity


class JobAggregate(object):

    def __init__(self, id,
                 name=None,
                 desc=None,
                 status=None,
                 start_time=None,
                 end_time=None):
        self.id = id
        self.name = name
        self.desc = desc
        self.status = status,
        self.start_time = start_time
        self.end_time = end_time
        self.task_list = []

    def add_task(self, task: TaskEntity):
        task.job_id = self.id
        self.task_list.append(task)

