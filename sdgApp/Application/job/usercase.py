import shortuuid

from sdgApp.Domain.job.job import JobAggregate
from sdgApp.Domain.job.task import TaskEntity
from sdgApp.Infrastructure.MongoDB.job.job_repoImpl import JobRepoImpl
from sdgApp.Infrastructure.Redis.job.job_queueImpl import JobQueueImpl


def dto_assembler(job: JobAggregate):
    return job.shortcut_DO

class JobCommandUsercase(object):

    def __init__(self, db_session, user, repo=JobRepoImpl, queue=JobQueueImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)
        self.queue = queue
    def create_job(self, dto: dict):
        try:
            uuid = shortuuid.uuid()
            job_dict = dto

            tasks_lst = job_dict["task_list"]
            job = JobAggregate(id=uuid,
                                name=job_dict["name"],
                                desc=job_dict["desc"])
            for task_dict in tasks_lst:
                task = TaskEntity(id=shortuuid.uuid(),
                                   name=task_dict['name'],
                                   desc=task_dict['desc'],
                                   car_id=task_dict['car_id'],
                                   car_name=task_dict['car_name'],
                                   scenario_id=task_dict['scenario_id'],
                                   scenario_name=task_dict["scenario_name"])
                job.add_task(task)
            self.repo.create(job)
            job = self.repo.get(job_id=uuid)
            if job:
                response_dto = dto_assembler(job)
                return response_dto
        except:
            raise

    def delete_job(self, job_id: str):
        try:
            self.repo.delete(job_id)
        except:
            raise

    def update_job(self, job_id:str, dto: dict):
        try:
            job_update_dict = dto
            tasks_lst = job_update_dict["task_list"]
            update_job = JobAggregate(id=job_id,
                                      name=job_update_dict["name"],
                                      desc=job_update_dict["desc"])
            for task_dict in tasks_lst:
                if task_dict['id']:
                    task_id = task_dict['id']
                else:
                    task_id = shortuuid.uuid()
                task = TaskEntity(id=task_id,
                                   name=task_dict['name'],
                                   desc=task_dict['desc'],
                                   car_id=task_dict['car_id'],
                                   car_name=task_dict['car_name'],
                                   scenario_id=task_dict['scenario_id'],
                                   scenario_name=task_dict["scenario_name"])
                update_job.add_task(task)

            self.repo.update(update_job)

            job = self.repo.get(job_id=job_id)
            if job:
                response_dto = dto_assembler(job)
                return response_dto
        except:
            raise

    def run_job(self, job_id:str, queue_sess):
        try:
            job = self.repo.get(job_id)
            if job:
                self.queue = self.queue(queue_sess)
                self.queue.publish(queue_name='tasks',
                                   job=job)

                response_dto = dto_assembler(job)
                return response_dto
        except:
            raise





class JobQueryUsercase(object):

    def __init__(self, db_session, user, repo=JobRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def get_job(self, job_id:str):
        try:
            job = self.repo.get(job_id)
            if job:
                response_dto = dto_assembler(job)
                return response_dto
        except:
            raise
        
    def list_job(self):
        try:
            response_dto_lst = []
            job_lst = self.repo.list()
            if job_lst:
                for job in job_lst:
                    response_dto = dto_assembler(job)
                    response_dto_lst.append(response_dto)
                return response_dto_lst
        except:
            raise



