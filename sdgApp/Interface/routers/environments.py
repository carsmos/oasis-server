from sdgApp.Application.envs.RespondsDTOs import EnvReadDTO
from sdgApp.Application.envs.CommandDTOs import EnvCreateDTO, EnvUpdateDTO
from sdgApp.Application.envs.usercase import EnvCommandUsercase, EnvQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from fastapi import APIRouter, status, Depends
from typing import List

router = APIRouter()


@router.post(
    "/envs",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvReadDTO,
    tags=["Envs"]
)
async def creat_env(env_create_model: EnvCreateDTO, db=Depends(get_db)):
    try:
        result = EnvCommandUsercase(db_session=db).create_env(env_create_model)
        return await find_specified_env(result, db)
    except:
        raise


@router.delete("/envs/{env_id}", tags=["Envs"])
async def delete_env(env_id: str, db=Depends(get_db)):
    try:
        return EnvCommandUsercase(db_session=db).delete_env(env_id)
    except:
        raise


@router.put(
    "/envs/{env_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=EnvReadDTO,
    tags=["Envs"]
)
async def update_env(env_id: str, env_update_model: EnvUpdateDTO, db=Depends(get_db)):
    try:
        result = EnvCommandUsercase(db_session=db).update_env(env_id, env_update_model)
        if result:
            return await find_specified_env(env_id, db)
    except:
        raise


@router.get(
    "/envs",
    status_code=status.HTTP_200_OK,
    response_model=List[EnvReadDTO],
    tags=["Envs"]
)
async def find_all_envs(db=Depends(get_db)):
    try:
        return EnvQueryUsercase(db_session=db).find_all_envs()
    except:
        raise


@router.get(
    "/envs/{env_id}",
    status_code=status.HTTP_200_OK,
    response_model=EnvReadDTO,
    tags=["Envs"]
)
async def find_specified_env(env_id: str, db=Depends(get_db)):
    try:
        return EnvQueryUsercase(db_session=db).find_specified_env(env_id)
    except:
        raise
