from datetime import datetime

from sdgApp.Domain.job.job import JobAggregate
from sdgApp.Domain.job.job_repo import JobRepo


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    ...


class JobRepoImpl(JobRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.job_collection = self.db_session['job']
        self.scen_collection = self.db_session['scenarios']

    def create(self, job: JobAggregate):
        task_DO_list = []
        filter = {"usr_id": self.user.id}
        for task_DO in job.task_list:
            scenario_id = task_DO['scenario_id']
            scen_dict = self.scen_collection.find_one(filter, {'_id': 0, 'scenario_param': 1})
            if scen_dict:
                task_DO.update(scen_dict)
            else:
                task_DO.update({'scenario_param': None})
            task_DO_list.append(task_DO)

        job_DO = {"id":job.id,
                  "name":job.name,
                  "desc":job.desc,
                  "task_list":task_DO_list}

        job_DO.update({"usr_id": self.user.id})
        job_DO.update({"create_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       "last_modified": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

        self.job_collection.insert_one(job_DO)

    def delete(self, job_id: str):
        filter = {'id': job_id}
        filter.update({"usr_id": self.user.id})

        self.job_collection.delete_one(filter)

    def update(self, update_job: JobAggregate):
        task_DO_list = []
        filter = {"usr_id": self.user.id}
        for task_DO in update_job.task_list:
            scenario_id = task_DO['scenario_id']
            scen_dict = self.scen_collection.find_one(filter, {'_id': 0, 'scenario_param': 1})
            if scen_dict:
                task_DO.update(scen_dict)
            else:
                task_DO.update({'scenario_param': None})
            task_DO_list.append(task_DO)

        update_job_DO = {"name": update_job.name,
                         "desc": update_job.desc,
                         "task_list": task_DO_list}


        update_job_DO.update({"last_modified": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

        filter = {
            'id': update_job.id
        }
        filter.update({"usr_id": self.user.id})
        self.job_collection.update_one(filter
                                           , {'$set': update_job_DO})

    def get(self, job_id: str):
        filter = {'id': job_id}
        filter.update({"usr_id": self.user.id})

        result_DO = self.job_collection.find_one(filter, {'_id': 0, 'usr_id': 0})
        if result_DO:
            job = JobAggregate(id=result_DO["id"])
            job.save_DO_shortcut(result_DO)
            return job

    def list(self):
        filter = {"usr_id": self.user.id}

        job_aggregate_lst = []
        results_DO = self.job_collection.find(filter, {'_id': 0, 'usr_id': 0})
        if results_DO:
            for one_result in results_DO:
                one_job = JobAggregate(id=one_result["id"])
                one_job.save_DO_shortcut(one_result)
                job_aggregate_lst.append(one_job)
            return job_aggregate_lst
