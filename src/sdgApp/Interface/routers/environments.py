from sdgApp.Application.environments.RespondsDTOs import EnvReadDTO
from sdgApp.Application.environments.CommandDTOs import EnvCreateDTO, EnvUpdateDTO
from sdgApp.Application.environments.usercase import EnvCommandUsercase, EnvQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from fastapi import APIRouter, status, Depends
from sdgApp.Infrastructure.MongoDB.FastapiUsers.users_model import UserDB
from sdgApp.Infrastructure.MongoDB.FastapiUsers.manager import current_active_user
from typing import List

router = APIRouter()


@router.post(
    "/environments",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvReadDTO,
    tags=["Envs"]
)
async def creat_env(env_create_model: EnvCreateDTO, db=Depends(get_db),
                    user: UserDB = Depends(current_active_user)):
    try:
        EnvCommandUsercase(db_session=db, user=user).create_env(env_create_model)
    except:
        raise


@router.delete("/environments/{env_id}",
               status_code=status.HTTP_202_ACCEPTED,
               tags=["Envs"])
async def delete_env(env_id: str, db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        EnvCommandUsercase(db_session=db, user=user).delete_env(env_id)
    except:
        raise


@router.put(
    "/environments/{env_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=EnvReadDTO,
    tags=["Envs"]
)
async def update_env(env_id: str, env_update_model: EnvUpdateDTO, db=Depends(get_db),
                     user: UserDB = Depends(current_active_user)):
    try:
        EnvCommandUsercase(db_session=db, user=user).update_env(env_id, env_update_model)
    except:
        raise

@router.get(
    "/environments/{env_id}",
    status_code=status.HTTP_200_OK,
    response_model=EnvReadDTO,
    tags=["Envs"]
)
async def find_specified_env(env_id: str, db=Depends(get_db),
                             user: UserDB = Depends(current_active_user)):
    try:
        return EnvQueryUsercase(db_session=db, user=user).find_specified_env(env_id)
    except:
        raise


@router.get(
    "/environments",
    status_code=status.HTTP_200_OK,
    response_model=List[EnvReadDTO],
    tags=["Envs"]
)
async def find_all_envs(skip: int = 0, db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return EnvQueryUsercase(db_session=db, user=user).find_all_envs(skip)
    except:
        raise



