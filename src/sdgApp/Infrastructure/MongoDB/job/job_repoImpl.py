from datetime import datetime

from sdgApp.Domain.job.job import JobAggregate
from sdgApp.Domain.job.job_repo import JobRepo
from sdgApp.Infrastructure.MongoDB.job.job_DO import JobDO, TaskDO


class JobRepoImpl(JobRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.job_collection = self.db_session['job']
        self.scen_collection = self.db_session['scenarios']
        self.car_collection = self.db_session['cars']

    async def create(self, job: JobAggregate):
        task_DO_list = []
        for task in job.task_list:
            # get scenario snapshot
            filter = {'id': task.scenario_id}
            scen_dict = await self.scen_collection.find_one(filter, {'_id': 0, 'scenario_param': 1})
            # get car and sensor snapshot
            filter = {'id': task.car_id}
            car_snap = await self.car_collection.find_one(filter, {'_id': 0, 'car_snap': 1})
            sensors_snap = await self.car_collection.find_one(filter, {'_id': 0, 'sensors_snap': 1})

            task_DO_list.append(TaskDO(id=task.id,
                                       name=task.name,
                                       desc=task.desc,
                                       car_id=task.car_id,
                                       car_name=task.car_name,
                                       scenario_id=task.scenario_id,
                                       scenario_name=task.scenario_name,
                                       result=task.result,
                                       job_id=task.job_id,
                                       status=task.status,
                                       replay_url=task.replay_url,
                                       cam_url=task.cam_url,
                                       scenario_param=scen_dict['scenario_param'],
                                       car_snap=car_snap['car_snap'],
                                       sensors_snap=sensors_snap['sensors_snap']
                                       ))

        job_DO = JobDO(id=job.id,
                       name=job.name,
                       desc=job.desc,
                       usr_id=self.user.id,
                       create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       task_list=task_DO_list)

        await self.job_collection.insert_one(job_DO.dict())

    async def delete(self, job_id: str):
        filter = {'id': job_id}
        filter.update({"usr_id": self.user.id})

        await self.job_collection.delete_one(filter)

    async def update(self, update_job: JobAggregate):
        task_DO_list = []
        for task in update_job.task_list:
            # get scenario snapshot
            filter = {'id': task.scenario_id}
            scen_dict = await self.scen_collection.find_one(filter, {'_id': 0, 'scenario_param': 1})
            # get car and sensor snapshot
            filter = {'id': task.car_id}
            car_snap = await self.car_collection.find_one(filter, {'_id': 0, 'car_snap': 1})
            sensors_snap = await self.car_collection.find_one(filter, {'_id': 0, 'sensors_snap': 1})

            task_DO_list.append(TaskDO(id=task.id,
                                       name=task.name,
                                       desc=task.desc,
                                       car_id=task.car_id,
                                       car_name=task.car_name,
                                       scenario_id=task.scenario_id,
                                       scenario_name=task.scenario_name,
                                       result=task.result,
                                       job_id=task.job_id,
                                       status=task.status,
                                       replay_url=task.replay_url,
                                       cam_url=task.cam_url,
                                       scenario_param=scen_dict['scenario_param'],
                                       car_snap=car_snap['car_snap'],
                                       sensors_snap=sensors_snap['sensors_snap']
                                       ))

        update_job_DO = JobDO(id=update_job.id,
                       name=update_job.name,
                       desc=update_job.desc,
                       usr_id=None,
                       create_time=None,
                       last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       task_list=task_DO_list)

        filter = {
                'id': update_job.id
            }
        filter.update({"usr_id": self.user.id})
        await self.job_collection.update_one(filter
                                       , {'$set': update_job_DO.dict(exclude={'usr_id','create_time'})})

    async def get(self, job_id: str):
        filter = {'id': job_id}
        filter.update({"usr_id": self.user.id})

        result_dict = await self.job_collection.find_one(filter, {'_id': 0})
        if result_dict:
            job = JobDO(**result_dict).to_entity()
            return job

    async def list(self):
        filter = {"usr_id": self.user.id}
        job_aggregate_lst = []
        results_dict = self.job_collection.find(filter, {'_id': 0})
        if results_dict:
            async for one_result in results_dict:
                one_job = JobDO(**one_result).to_entity()
                job_aggregate_lst.append(one_job)
            return job_aggregate_lst
