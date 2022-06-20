from sdgApp.Application.dynamic_scenes.RespondsDTOs import DynamicSceneReadDTO, DynamicScenesResponse
from sdgApp.Application.dynamic_scenes.CommandDTOs import DynamicSceneCreateDTO, DynamicSceneUpdateDTO
from sdgApp.Application.dynamic_scenes.usercase import DynamicSceneCommandUsercase, DynamicSceneQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from fastapi import APIRouter, status, Depends
from sdgApp.Interface.FastapiUsers.users_model import UserDB
from sdgApp.Interface.FastapiUsers.manager import current_active_user
from typing import List
from sdgApp.Application.log.usercase import except_logger
router = APIRouter()


@router.post(
    "/dynamic_scenes",
    status_code=status.HTTP_201_CREATED,
    response_model=DynamicSceneReadDTO,
    tags=["DynamicScenes"]
)
@except_logger("create_dynamic_scene failed .....................")
async def create_dynamic_scene(dynamic_scene_create_model: DynamicSceneCreateDTO,
                               db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        await DynamicSceneCommandUsercase(db_session=db, user=user).create_scenario(dynamic_scene_create_model)
    except:
        raise


@router.delete("/dynamic_scenes/{dynamic_scene_id}",
               status_code=status.HTTP_202_ACCEPTED,
               tags=["DynamicScenes"])
@except_logger("delete_dynamic_scene failed .....................")
async def delete_dynamic_scene(dynamic_scene_id: str, db=Depends(get_db),
                               user: UserDB = Depends(current_active_user)):
    try:
        await DynamicSceneCommandUsercase(db_session=db, user=user).delete_scenario(dynamic_scene_id)
    except:
        raise


@router.put(
    "/dynamic_scenes/{dynamic_scene_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=DynamicSceneReadDTO,
    tags=["DynamicScenes"]
)
@except_logger("update_dynamic_scene failed .....................")
async def update_dynamic_scene(dynamic_scene_id: str,
                               dynamic_scene_update_model: DynamicSceneUpdateDTO,
                               db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        await DynamicSceneCommandUsercase(db_session=db, user=user).update_scenario(dynamic_scene_id,
                                                                              dynamic_scene_update_model)
    except:
        raise


@router.get(
    "/dynamic_scenes",
    status_code=status.HTTP_200_OK,
    response_model=DynamicScenesResponse,
    tags=["DynamicScenes"]
)
@except_logger("find_all_dynamic_scenes failed .....................")
async def find_all_dynamic_scenes(skip: int = 1, p_size: int = 15, content: str = "", db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return await DynamicSceneQueryUsercase(db_session=db, user=user).find_all_scenarios(skip, p_size, content)
    except:
        raise


@router.get(
    "/dynamic_scenes/{dynamic_scene_id}",
    status_code=status.HTTP_200_OK,
    response_model=DynamicSceneReadDTO,
    tags=["DynamicScenes"]
)
@except_logger("find_specified_scenario failed .....................")
async def find_specified_scenario(dynamic_scene_id: str, db=Depends(get_db),
                                  user: UserDB = Depends(current_active_user)):
    try:
        return await DynamicSceneQueryUsercase(db_session=db, user=user).find_specified_scenario(dynamic_scene_id)
    except:
        raise
