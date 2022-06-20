class TaskEntity(object):

    def __init__(self, id,
                 name,
                 desc,
                 car_id,
                 car_name,
                 scenario_id,
                 scenario_name,
                 job_id="",
                 result="",
                 status="notrun",
                 index=None,
                 replay_url=None,
                 original_id=None,
                 cam_url=None,
                 last_modified=None,
                 start_time=None,
                 end_time=None):
        self.id = id
        self.name = name
        self.desc = desc
        self.car_id = car_id
        self.car_name = car_name
        self.scenario_id = scenario_id
        self.scenario_name = scenario_name
        self.job_id = job_id
        self.result = result
        self.status = status
        self.replay_url = replay_url
        self.cam_url = cam_url
        self.retry_id = original_id
        self.last_modified = last_modified
        self.index = index
        self.start_time = start_time
        self.end_time = end_time


