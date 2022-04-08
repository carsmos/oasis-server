import shortuuid

from sdgApp.Application.car.usercase import split_page
from sdgApp.Domain.job.job import JobAggregate
from sdgApp.Domain.job.task import TaskEntity
from sdgApp.Infrastructure.MongoDB.job.job_repoImpl import JobRepoImpl
from sdgApp.Infrastructure.Redis.job.job_queueImpl import JobQueueImpl
from sdgApp.Application.job.CommandDTOs import JobCreateDTO, JobUpdateDTO
from sdgApp.Application.job.RespondsDTOs import JobReadDTO


def dto_assembler(job: JobAggregate):
    return job.shortcut_DO

class JobCommandUsercase(object):

    def __init__(self, db_session, user, repo=JobRepoImpl, queue=JobQueueImpl):
        self.db_session = db_session
        self.user = user
        self.job_collection = self.db_session['job']
        self.repo = repo
        self.repo = self.repo(db_session, user)
        self.queue = queue
    async def create_job(self, job_create_model: JobCreateDTO):
        try:
            uuid = shortuuid.uuid()

            tasks_lst = job_create_model.task_list
            job = JobAggregate(id=uuid,
                                name=job_create_model.name,
                                desc=job_create_model.desc)
            for task_model in tasks_lst:
                task = TaskEntity(id=shortuuid.uuid(),
                                   name=task_model.name,
                                   desc=task_model.desc,
                                   car_id=task_model.car_id,
                                   car_name=task_model.car_name,
                                   scenario_id=task_model.scenario_id,
                                   scenario_name=task_model.scenario_name)
                job.add_task(task)
            await self.repo.create(job)
        except:
            raise

    async def delete_job(self, job_id: str):
        try:
            await self.repo.delete(job_id)
        except:
            raise

    async def update_job(self, job_id:str, job_update_model: JobUpdateDTO):
        ## ! update finished job can cause status and replay url loss
        try:
            job_retrieved = self.repo.get(job_id=job_id)
            tasks_lst = job_update_model.task_list
            job_retrieved.name = job_update_model.name
            job_retrieved.desc = job_update_model.desc
            job_retrieved.task_list = []

            for task_model in tasks_lst:
                if task_model.id:
                    task_id = task_model.id
                else:
                    task_id = shortuuid.uuid()
                task = TaskEntity(id=task_id,
                                   name=task_model.name,
                                   desc=task_model.desc,
                                   car_id=task_model.car_id,
                                   car_name=task_model.car_name,
                                   scenario_id=task_model.scenario_id,
                                   scenario_name=task_model.scenario_name)
                job_retrieved.add_task(task)

            await self.repo.update(job_retrieved)
        except:
            raise

    async def run_job(self, job_id:str, queue_sess):
        try:
            filter = {'id': job_id}
            filter.update({"usr_id": self.user.id})
            result_dict = await self.job_collection.find_one(filter, {'_id': 0})
            if result_dict:
                self.queue = self.queue(queue_sess)
                self.queue.publish(queue_name='tasks',
                                   job=result_dict)
        except:
            raise





class JobQueryUsercase(object):

    def __init__(self, db_session, user, repo=JobRepoImpl):
        self.db_session = db_session
        self.user = user
        self.job_collection = self.db_session['job']

    async def get_job(self, job_id:str):
        try:
            filter = {'id': job_id}
            filter.update({"usr_id": self.user.id})

            result_dict = await self.job_collection.find_one(filter, {'_id': 0, 'usr_id':0})
            return JobReadDTO(**result_dict)
        except:
            raise

    async def list_job(self, p_num):
        try:
            response_dto_lst = []
            filter = {"usr_id": self.user.id}
            results_dict = self.job_collection.find(filter, {'_id': 0, 'usr_id': 0}).sort([('last_modified', -1)])
            if results_dict:
                async for one_result in results_dict:
                    response_dto_lst.append(JobReadDTO(**one_result))

                response_dto_lst = split_page(p_num, response_dto_lst)
                return response_dto_lst
        except:
            raise



