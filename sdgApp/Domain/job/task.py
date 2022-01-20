class TaskEntity(object):

    def __init__(self, id,
                 name,
                 desc,
                 car_id,
                 car_name,
                 scenario_id,
                 scenario_name):
        self.id = id
        self.job_id = ""
        self.name = name
        self.desc = desc
        self.car_id = car_id
        self.car_name = car_name
        self.scenario_id = scenario_id
        self.scenario_name = scenario_name
        self.result = "no result"

    def attach_to(self, job_id):
        self.job_id = job_id

    def write_result(self, result):
        self.result = result