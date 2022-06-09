import datetime
import math

import shortuuid

from sdgApp.Domain.job.job import JobAggregate
from sdgApp.Domain.job.task import TaskEntity
from sdgApp.Infrastructure.MongoDB.job.job_repoImpl import JobRepoImpl
from sdgApp.Infrastructure.Redis.job.job_queueImpl import JobQueueImpl
from sdgApp.Application.job.CommandDTOs import JobCreateDTO, JobUpdateDTO
from sdgApp.Application.job.RespondsDTOs import JobReadDTO

from sdgApp.Application.car.usercase import CarQueryUsercase
from sdgApp.Domain.car.car_exceptions import CarNotFoundError
from sdgApp.Application.scenarios.usercase import ScenarioQueryUsercase
from sdgApp.Domain.scenarios.scenarios_exceptions import ScenarioNotFoundError

from sdgApp.Application.job.utils import handle_finish_pass_job


def dto_assembler(job: JobAggregate):
    return job.shortcut_DO


class JobCommandUsercase(object):

    def __init__(self, db_session, user, repo=JobRepoImpl):
        self.db_session = db_session
        self.user = user
        self.job_collection = self.db_session['job']
        self.repo = repo
        self.repo = self.repo(db_session, user)
        self.queue = None

    async def create_job(self, job_create_model: JobCreateDTO):
        try:
            uuid = shortuuid.uuid()
            tasks_lst = job_create_model.task_list
            job = JobAggregate(id=uuid,
                                name=job_create_model.name,
                                desc=job_create_model.desc,
                                status='waiting')
            for task_model in tasks_lst:

                await CarQueryUsercase(db_session=self.db_session, user=self.user).get_car(task_model.car_id)
                await ScenarioQueryUsercase(db_session=self.db_session, user=self.user).find_specified_scenario(task_model.scenario_id)

                task = TaskEntity(id=shortuuid.uuid(),
                                   name=task_model.name,
                                   desc=task_model.desc,
                                   car_id=task_model.car_id,
                                   car_name=task_model.car_name,
                                   scenario_id=task_model.scenario_id,
                                   scenario_name=task_model.scenario_name)
                job.add_task(task)
            await self.repo.create(job)

        except CarNotFoundError:
            raise

        except ScenarioNotFoundError:
            raise

        except:
            raise

    async def delete_job(self, job_id: str):
        try:
            await self.repo.delete(job_id)
        except:
            raise

    async def delete_task(self, job_id: str, task_ids: str):
        try:
            filter = {'id': job_id}
            filter.update({"usr_id": self.user.id})
            job = await self.job_collection.find_one(filter, {'_id': 0, 'usr_id': 0})
            task_list = job.get("task_list")
            task_id_list = task_ids.split(",")
            for task_id in task_id_list:
                for task in task_list[::-1]:
                    if task.get("id") == task_id:
                        task_list.remove(task)
            self.job_collection.update_one(filter, {'$set': job})
            return job
        except:
            raise

    async def update_job(self, job_id:str, job_update_model: JobUpdateDTO):
        ## ! update finished job can cause status and replay url loss
        try:
            job_retrieved = await self.repo.get(job_id=job_id)
            tasks_lst = job_update_model.task_list
            job_retrieved.name = job_update_model.name
            job_retrieved.desc = job_update_model.desc
            job_retrieved.task_list = []

            for task_model in tasks_lst:

                await CarQueryUsercase(db_session=self.db_session, user=self.user).get_car(task_model.car_id)
                await ScenarioQueryUsercase(db_session=self.db_session, user=self.user).find_specified_scenario(
                    task_model.scenario_id)

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

        except CarNotFoundError:
            raise

        except ScenarioNotFoundError:
            raise

        except:
            raise

    async def run_job(self, job_id: str, queue_sess):
        try:
            filter = {'id': job_id}
            filter.update({"usr_id": self.user.id})
            result_dict = await self.job_collection.find_one(filter, {'_id': 0})
            if result_dict:
                self.queue = JobQueueImpl(queue_sess)
                self.queue.publish(result_dict)
                self.update_task_status(result_dict, filter, "inqueue", 'start')
                self.update_job_status_inqueue(filter)
        except:
            raise

    def update_task_status(self, result_dict, filter, status, start_or_end, task_id=None):
        try:
            if task_id:
                for task in result_dict.get('task_list'):
                    if task.get("id") == task_id:
                        task['status'] = status
            else:
                for task in result_dict.get('task_list'):
                    task['status'] = status
            if start_or_end == 'start':
                result_dict['start_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if start_or_end == 'end':
                result_dict['end_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.job_collection.update_one(filter, {'$set': result_dict})
        except:
            raise

    def update_job_status_inqueue(self, filter):
        try:
            self.job_collection.update_one(filter, {'$set': {'status': 'inqueue'}})
        except:
            raise

    async def stop_jobs(self, job_ids: str, queue_sess):
        try:
            for job_id in job_ids.split("+"):
                filter = {'id': job_id}
                filter.update({"usr_id": self.user.id})
                result_dict = await self.job_collection.find_one(filter, {'_id': 0})
                if result_dict:
                    self.queue = JobQueueImpl(queue_sess)
                    self.queue.delete(job=result_dict)
                    self.update_task_status(result_dict, filter, "notrun", "end")
        except:
            raise

    async def retry_task(self, job_id, task_ids, queue_sess):
        try:
            filter = {'id': job_id}
            filter.update({"usr_id": self.user.id})
            result_dict = await self.job_collection.find_one(filter, {'_id': 0})
            if result_dict:
                self.queue = JobQueueImpl(queue_sess)
                job = self.queue.add(result_dict, task_ids)
                self.job_collection.update_one(filter, {'$set': job})
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

            result_dict = await self.job_collection.find_one(filter, {'_id': 0, 'usr_id': 0})
            jobReadDTO = JobReadDTO(**result_dict)
            jobReadDTO = handle_finish_pass_job(jobReadDTO)
            return jobReadDTO
        except:
            raise

    async def list_job(self, pagenum, pagesize, asc, status, content):
        try:
            filter = {"usr_id": self.user.id}
            if status:
                if status == "running":
                    filter.update({"$or": [{"status": "running"}, {"status": "inqueue"}]})
                else:
                    filter.update({"status": status})
            if content:
                filter.update({"$or": [{"name": {"$regex": content, "$options": "$i"}}, {"desc": {"$regex": content, "$options": "$i"}}]})

            total_num = await self.job_collection.count_documents(filter)
            total_page_num = math.ceil(total_num / pagesize)
            if pagenum > total_page_num > 0:
                pagenum = total_page_num
            if pagenum > 0:
                results_dict = self.job_collection.find(filter, {'_id': 0, 'usr_id': 0}).sort([('last_modified', int(asc))]).skip((pagenum-1) * pagesize).limit(pagesize).to_list(length=50)
            else:
                results_dict = self.job_collection.find(filter, {'_id': 0, 'usr_id': 0}).sort([('last_modified', int(asc))]).to_list(length=total_num)
            if results_dict:
                response_dic = {}
                response_dto_lst = []
                response_dic["total_num"] = total_num
                response_dic["total_page_num"] = total_page_num

                for doc in await results_dict:
                    jobReadDTO = JobReadDTO(**doc)
                    jobReadDTO = handle_finish_pass_job(jobReadDTO)
                    response_dto_lst.append(jobReadDTO)
                response_dic["datas"] = response_dto_lst
                return response_dic
        except:
            raise

    @staticmethod
    def handle_job_status(status, response_dto_lst):
        finished_job_list = []
        running_job_list = []
        notrun_job_list = []
        finished_status_list = ["Finish", "timeout"]

        for job in response_dto_lst:
            isruning = any([task.get("status") in ["inqueue", "isRunning"] for task in job.task_list])
            if isruning:
                running_job_list.append(job)
            # for task in job.task_list:
            #     if task.get("status") in ["inqueue", "isRunning"]:
            #         running_job_list.append(job)
            #         break
        for job in [job for job in response_dto_lst if job not in running_job_list]:
            not_run = all([task.get("status") in ['notrun', "Not running"] for task in job.task_list])
            if not_run:
                notrun_job_list.append(job)

        for job in [job for job in response_dto_lst if job not in running_job_list+notrun_job_list]:
            hasfinished = all([task.get("status") in finished_status_list for task in job.task_list])
            if hasfinished:
                finished_job_list.append(job)
            # all_length = len(job.task_list)
            # finish_length = len([task for task in job.task_list if task.get("status") in finished_status_list])
            # if all_length == finish_length:
            #     finished_job_list.append(job)

        if status == "finished":
            return finished_job_list
        elif status == "notrun":
            return notrun_job_list
        elif status == "running":
            return running_job_list

    async def get_total_task_info(self, queue_sess):
        try:
            filter = {"usr_id": self.user.id}
            results_dict = self.job_collection.find(filter).to_list(length=1000000)
            ret_dic = {}
            failure_num = 0
            success_num = 0

            for job_dic in await results_dict:
                success_num += len([task for task in job_dic.get('task_list') if task.get("status") == "Finish"])
                failure_num += len([task for task in job_dic.get('task_list') if task.get("status") in ["timeout"]])
            ret_dic["success_task_num"] = success_num
            ret_dic["failure_task_num"] = failure_num

            # 获取排队中的任务数量
            queue = JobQueueImpl(queue_sess)
            queue_num = queue.get_length()
            ret_dic["queue_num"] = queue_num

            return ret_dic
        except:
            raise

    async def get_jobs_infos(self, status, cycle, name, p_num, limit, asc):
        try:
            filter = {"usr_id": self.user.id}
            if cycle in ["day", "week", "month"]:
                filter = self.get_times(cycle, filter)
            if name not in [""]:
                filter.update({"$or": [{"name": {"$regex": name}}, {"desc": {"$regex": name}}]})
            total_num = await self.job_collection.count_documents(filter)
            total_page_num = math.ceil(total_num / limit)
            if p_num > total_page_num and total_page_num > 0:
                p_num = total_page_num
            if p_num > 0:
                results = self.job_collection.find(filter, {'_id': 0, 'usr_id': 0}).\
                    sort([('last_modified', int(asc))]).skip((p_num-1) * limit).limit(limit).to_list(length=50)
            else:
                results = self.job_collection.find(filter, {'_id': 0, 'usr_id': 0}).\
                    sort([('last_modified', int(asc))]).to_list(length=total_num)
            if results:
                response_dic = {}
                response_dto_lst = []

                for doc in await results:
                    response_dto_lst.append(JobReadDTO(**doc))
                if status not in ["all"]:
                    response_dto_lst = self.handle_job_status(status, response_dto_lst)
                    total_num = len(response_dto_lst)
                    total_page_num = math.ceil(total_num / limit)
                response_dic["datas"] = response_dto_lst
                response_dic["total_num"] = total_num
                response_dic["total_page_num"] = total_page_num
                return response_dic
        except:
            raise

    def get_times(self, cycle, filter):
        now = datetime.datetime.now()
        if cycle == "day":
            zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.minute,
                                                 microseconds=now.microsecond)
            zero_time = datetime.datetime.strftime(zero, '%Y-%m-%d %H:%M:%S')
            last = zero + datetime.timedelta(hours=23, minutes=59, seconds=59)
            last_time = datetime.datetime.strftime(last, '%Y-%m-%d %H:%M:%S')
            # {"last_modified": {"$gte":"2022-05-30 00:00:40", "$lte":"2022-05-31 00:00:39"}}
            filter.update({"last_modified": {"$gte": zero_time, "$lte": last_time}})
        elif cycle == "week":
            zero = now - datetime.timedelta(days=now.weekday(), hours=now.hour, minutes=now.minute,
                                                 seconds=now.minute, microseconds=now.microsecond)
            zero_time = datetime.datetime.strftime(zero, '%Y-%m-%d %H:%M:%S')
            last = now + datetime.timedelta(days=6 - now.weekday(), hours=23 - now.hour, minutes=59 - now.minute,
                                                 seconds=59 - now.minute)
            last_time = datetime.datetime.strftime(last, '%Y-%m-%d %H:%M:%S')
            filter.update({"last_modified": {"$gte": zero_time, "$lte": last_time}})
        elif cycle == "month":
            zero = datetime.datetime(now.year, now.month, 1)
            zero_time = datetime.datetime.strftime(zero, '%Y-%m-%d %H:%M:%S')
            last = datetime.datetime(now.year, now.month + 1, 1) - datetime.timedelta(days=1) + \
                        datetime.timedelta(hours=23, minutes=59, seconds=59)
            last_time = datetime.datetime.strftime(last, '%Y-%m-%d %H:%M:%S')
            filter.update({"last_modified": {"$gte": zero_time, "$lte": last_time}})
        return filter
