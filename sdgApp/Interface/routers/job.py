from fastapi import APIRouter, status, Depends

from sdgApp.Application.job.CommandDTOs import JobCreateDTO, JobUpdateDTO
from sdgApp.Application.job.usercase import JobCommandUsercase, JobQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from sdgApp.Infrastructure.Redis.session_maker import get_redis
from sdgApp.Infrastructure.MongoDB.FastapiUsers.users_model import UserDB
from sdgApp.Infrastructure.MongoDB.FastapiUsers.manager import current_active_user

router = APIRouter()

@router.post(
    "/job",
    status_code=status.HTTP_201_CREATED,
    tags=["Job"]
)
async def create_job(job_create_model: JobCreateDTO, db = Depends(get_db),
                          user: UserDB = Depends(current_active_user)):
    try:
        job_create_dto = job_create_model.dict()
        job_dto = JobCommandUsercase(db_session=db, user=user).create_job(job_create_dto)
        return job_dto
    except:
        raise
    
    
@router.delete(
    "/job/{job_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Job"]
)
async def delete_job(job_id:str, db = Depends(get_db),
                          user: UserDB = Depends(current_active_user)):
    try:
        JobCommandUsercase(db_session=db, user=user).delete_job(job_id)
    except:
        raise
    
@router.put(
    "/job/{job_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Job"]
)
async def update_job(job_id:str, job_update_model: JobUpdateDTO, db = Depends(get_db),
                          user: UserDB = Depends(current_active_user)):
    try:
        job_update_dto = job_update_model.dict()
        job_dto = JobCommandUsercase(db_session=db, user=user).update_job(job_id, job_update_dto)
        return job_dto
    except:
        raise


@router.get(
    "/job/{job_id}",
    status_code=status.HTTP_200_OK,
    # response_model= JobGetDTO,
    tags=["Job"]
)
async def get_job(job_id:str, db = Depends(get_db),
                       user: UserDB = Depends(current_active_user)):
    try:
        job_dto = JobQueryUsercase(db_session=db, user=user).get_job(job_id)
        return job_dto
    except:
        raise
    

@router.get(
    "/job",
    status_code=status.HTTP_200_OK,
    # response_model= List[CarGetDTO],
    tags=["Job"]
)
async def list_job(db = Depends(get_db),
                   user: UserDB = Depends(current_active_user)):
    try:
        job_dto_lst = JobQueryUsercase(db_session=db, user=user).list_job()
        return job_dto_lst
    except:
        raise

@router.get(
    "/run-job/{job_id}",
    status_code=status.HTTP_200_OK,
    # response_model= List[CarGetDTO],
    tags=["Job"]
)
async def run_job(job_id:str, db = Depends(get_db), queue_sess = Depends(get_redis),
                   user: UserDB = Depends(current_active_user)):
    try:
        job_dto = JobCommandUsercase(db_session=db, user=user).run_job(job_id, queue_sess)
        return job_dto
    except:
        raise
