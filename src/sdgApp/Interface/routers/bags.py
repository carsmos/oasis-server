from fastapi import APIRouter, status, Depends
from typing import Optional
from sdgApp.Infrastructure.Redis.session_maker import get_redis
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from sdgApp.Interface.FastapiUsers.users_model import UserDB
from sdgApp.Interface.FastapiUsers.manager import current_active_user
from sdgApp.Application.job.usercase import JobQueryUsercase
import json
from sdgApp.Application.job.RespondsDTOs import JobReadDTO, JobStatusMsg, JobsResponse

router = APIRouter()



@router.post(
    "/bags/{job_id}/{task_id}",
    status_code=status.HTTP_200_OK,
    tags=["Bags"]
)
async def upload(job_id: str, task_id: str, redis=Depends(get_redis), mongo=Depends(get_db),
                   user: UserDB = Depends(current_active_user)):
    try:
        job_dto = await JobQueryUsercase(db_session=mongo, user=user).get_job(job_id)
        if job_dto is None or all([task_id != str(task["id"]) for task in job_dto.task_list]):
            return {"code":"1", "msg": "bad request!"}

        # this method have concurrency issues, maybe relation db is a better choice
        job = await mongo['job'].find_one({"id": job_id})
        for task in job['task_list']:
            if task_id == str(task["id"]):
                if 'process_rate' not in task.keys() or task['process_rate'] != '-1':
                    return {"code":"2", "msg": "this bag is processing!"}
                task['process_rate'] = '0'
                result = await mongo['job'].update_one({'id': job_id}, {'$set': job})

        redis.lpush("bag_upload", json.dumps({"task_id": task_id, "job_id": job_id}))
        return {"code":"0", "msg": "success"}
    except:
        raise


# @router.get(
#     "/bags/{job_id}/{task_id}",
#     status_code=status.HTTP_200_OK,
#     tags=["Bags"]
# )
# async def get_progress(job_id: str, task_id: str, redis=Depends(get_redis), mongo=Depends(get_db),
#                    user: UserDB = Depends(current_active_user)):
#     try:
#         job_dto = await JobQueryUsercase(db_session=mongo, user=user).get_job(job_id)
#         if job_dto is None or all([task_id != str(task["id"]) for task in job_dto.task_list]):
#             return {"msg": "bad request!"}

#         for task in job_dto.task_list:
#             if task_id == str(task["id"]):
#                 if 'process_rate' in task.keys():
#                     return {"percentage" : task["process_rate"]}
#                 return {"percentage" : '0'}
#         return {"msg": "bad request!"}
#     except:
#         raise