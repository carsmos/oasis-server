from sdgApp.Application.envs.RespondsDTOs import EnvReadDTO
from sdgApp.Application.envs.CommandDTOs import EnvCreateDTO, EnvUpdateDTO
from sdgApp.Application.envs.usercase import EnvCommandUsercase, \
    EnvDeleteUsercase, EnvUpdateUsercase, EnvQueryUsercase
from fastapi import APIRouter, status
from typing import List

router = APIRouter()


@router.post(
    "/envs",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvReadDTO,
    tags=["Envs"]
)
async def creat_env(env_create_model: EnvCreateDTO):
    try:
        return EnvCommandUsercase().create_env(env_create_model)
    except:
        raise


@router.delete("/envs/{env_id}", tags=["Envs"])
async def delete_env(env_id: str):
    try:
        return EnvDeleteUsercase().delete_env(env_id)
    except:
        raise


@router.put(
    "/envs/{env_id}",
    response_model=EnvReadDTO,
    tags=["Envs"]
)
async def update_env(env_id: str, env_update_model: EnvUpdateDTO):
    try:
        return EnvUpdateUsercase().update_env(env_id, env_update_model)
    except:
        raise


@router.get(
    "/envs",
    status_code=status.HTTP_200_OK,
    response_model=List[EnvReadDTO],
    tags=["Envs"]
)
async def find_all_envs():
    try:
        return EnvQueryUsercase().find_all_envs()
    except:
        raise

@router.get(
    "/envs/{env_id}",
    status_code=status.HTTP_200_OK,
    response_model=EnvReadDTO,
    tags=["Envs"]
)
async def find_specified_env(env_id: str):
    try:
        return EnvQueryUsercase().find_specified_env(env_id)
    except:
        raise
