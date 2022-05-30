from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from pydantic.typing import List

from sdgApp.Application.job.CommandDTOs import JobCreateDTO, JobUpdateDTO
from sdgApp.Application.job.RespondsDTOs import JobReadDTO, JobStatusMsg, JobsResponse
from sdgApp.Application.job.usercase import JobCommandUsercase, JobQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from sdgApp.Infrastructure.Redis.session_maker import get_redis
from sdgApp.Interface.FastapiUsers.users_model import UserDB
from sdgApp.Interface.FastapiUsers.manager import current_active_user

from sdgApp.Domain.car.car_exceptions import CarNotFoundError
from sdgApp.Domain.scenarios.scenarios_exceptions import ScenarioNotFoundError

router = APIRouter()


@router.post(
    "/job",
    status_code=status.HTTP_201_CREATED,
    tags=["Job"]
)
async def create_job(job_create_model: JobCreateDTO, db=Depends(get_db),
                          user: UserDB = Depends(current_active_user)):
    try:
        await JobCommandUsercase(db_session=db, user=user).create_job(job_create_model)
    except CarNotFoundError as e:
        return JSONResponse(status_code=200, content={"status": "fail", "detail": e.message})
    except ScenarioNotFoundError as e:
        return JSONResponse(status_code=200, content={"status": "fail", "detail": e.message})
    except:
        raise
    
    
@router.delete(
    "/job/{job_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Job"]
)
async def delete_job(job_id: str, db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        await JobCommandUsercase(db_session=db, user=user).delete_job(job_id)
    except:
        raise


@router.delete(
    "/task/{job_id}/{task_ids}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Job"]
)
async def delete_task(job_id: str, task_ids: str, db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return await JobCommandUsercase(db_session=db, user=user).delete_task(job_id, task_ids)
    except:
        raise


@router.put(
    "/job/{job_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Job"]
)
async def update_job(job_id: str, job_update_model: JobUpdateDTO, db=Depends(get_db),
                          user: UserDB = Depends(current_active_user)):
    try:
        await JobCommandUsercase(db_session=db, user=user).update_job(job_id, job_update_model)
    except CarNotFoundError as e:
        return JSONResponse(status_code=200, content={"status": "fail", "detail": e.message})
    except ScenarioNotFoundError as e:
        return JSONResponse(status_code=200, content={"status": "fail", "detail": e.message})
    except:
        raise


@router.get(
    "/job/{job_id}",
    status_code=status.HTTP_200_OK,
    response_model=JobReadDTO,
    tags=["Job"]
)
async def get_job(job_id:str, db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        job_dto = await JobQueryUsercase(db_session=db, user=user).get_job(job_id)
        return job_dto
    except:
        raise
    

@router.get(
    "/job",
    status_code=status.HTTP_200_OK,
    response_model=JobsResponse,
    tags=["Job"]
)
async def list_job(skip: int = 1, limit: int = 15, asc: int = -1, db=Depends(get_db),
                   user: UserDB = Depends(current_active_user)):
    try:
        job_dto_dic = await JobQueryUsercase(db_session=db, user=user).list_job(skip, limit, asc)
        return job_dto_dic
    except:
        raise


@router.get(
    "/total_task_info",
    status_code=status.HTTP_200_OK,
    tags=["Job"]
)
async def get_total_task_info(db=Depends(get_db), user: UserDB = Depends(current_active_user), queue_sess=Depends(get_redis)):
    try:
        return await JobQueryUsercase(db_session=db, user=user).get_total_task_info(queue_sess)
    except:
        raise


@router.post(
    "/run-job/{job_id}",
    status_code=status.HTTP_200_OK,
    responses={200: {"model": JobStatusMsg}},
    tags=["Job"]
)
async def run_job(job_id: str, db=Depends(get_db), queue_sess=Depends(get_redis),
                   user: UserDB = Depends(current_active_user)):
    try:
        await JobCommandUsercase(db_session=db, user=user).run_job(job_id, queue_sess)
        return {"status":"success"}
    except:
        raise


@router.post(
    "/stop-jobs/{job_ids}",
    status_code=status.HTTP_200_OK,
    responses={200: {"model": JobStatusMsg}},
    tags=["Job"]
)
async def stop_jobs(job_ids: str, db=Depends(get_db), queue_sess=Depends(get_redis),
                    user: UserDB = Depends(current_active_user)):
    try:
        await JobCommandUsercase(db_session=db, user=user).stop_jobs(job_ids, queue_sess)
        return {"status": "success"}
    except:
        raise


@router.get(
    "/retry_task",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Job"]
)
async def retry_task(job_id: str, task_ids: str, db=Depends(get_db), queue_sess=Depends(get_redis),
                   user: UserDB = Depends(current_active_user)):
    try:
        await JobCommandUsercase(db_session=db, user=user).retry_task(job_id, task_ids, queue_sess)
        return {"status": "success"}
    except:
        raise


@router.get(
    "/job_infos",
    status_code=status.HTTP_200_OK,
    response_model=JobsResponse,
    tags=["Job"]
)
async def get_job_infos(status: str = "all", cycle: str = "", name: str = "",  skip: int = 1, limit: int = 15,
                        asc: int = -1, db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        job_dto_dic = await JobQueryUsercase(db_session=db, user=user).get_jobs_infos(status, cycle, name, skip, limit, asc)
        return job_dto_dic
    except:
        raise