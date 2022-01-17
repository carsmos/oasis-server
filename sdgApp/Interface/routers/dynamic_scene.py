from sdgApp.Application.dynamic_scenes.RespondsDTOs import DynamicSceneReadDTO
from sdgApp.Application.dynamic_scenes.CommandDTOs import DynamicSceneCreateDTO, DynamicSceneUpdateDTO
from sdgApp.Application.dynamic_scenes.usercase import DynamicSceneCommandUsercase, DynamicSceneQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from fastapi import APIRouter, status, Depends
from sdgApp.Infrastructure.MongoDB.FastapiUsers.users_model import UserDB
from sdgApp.Infrastructure.MongoDB.FastapiUsers.manager import current_active_user
from typing import List

router = APIRouter()


@router.post(
    "/dynamic_scenes",
    status_code=status.HTTP_201_CREATED,
    response_model=DynamicSceneReadDTO,
    tags=["DynamicScenes"]
)
async def create_dynamic_scene(dynamic_scene_create_model: DynamicSceneCreateDTO,
                               db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        dynamic_scene_create_dto = dynamic_scene_create_model.dict()
        result = DynamicSceneCommandUsercase(db_session=db, user=user).create_scenario(dynamic_scene_create_dto)
        return await find_specified_scenario(result, db)
    except:
        raise


@router.delete("/dynamic_scenes/{dynamic_scene_id}", tags=["DynamicScenes"])
async def delete_dynamic_scene(dynamic_scene_id: str, db=Depends(get_db),
                               user: UserDB = Depends(current_active_user)):
    try:
        return DynamicSceneCommandUsercase(db_session=db, user=user).delete_scenario(dynamic_scene_id)
    except:
        raise


@router.put(
    "/dynamic_scenes/{dynamic_scene_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=DynamicSceneReadDTO,
    tags=["DynamicScenes"]
)
async def update_dynamic_scene(dynamic_scene_id: str,
                               dynamic_scene_update_model: DynamicSceneUpdateDTO,
                               db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        dynamic_scene_update_dto = dynamic_scene_update_model.dict()
        result = DynamicSceneCommandUsercase(db_session=db, user=user).update_scenario(dynamic_scene_id,
                                                                       dynamic_scene_update_dto)
        if result:
            return await find_specified_scenario(dynamic_scene_id, db)
    except:
        raise


@router.get(
    "/dynamic_scenes",
    status_code=status.HTTP_200_OK,
    response_model=List[DynamicSceneReadDTO],
    tags=["DynamicScenes"]
)
async def find_all_dynamic_scenes(db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return DynamicSceneQueryUsercase(db_session=db, user=user).find_all_scenarios()
    except:
        raise


@router.get(
    "/dynamic_scenes/{dynamic_scene_id}",
    status_code=status.HTTP_200_OK,
    response_model=DynamicSceneReadDTO,
    tags=["DynamicScenes"]
)
async def find_specified_scenario(dynamic_scene_id: str, db=Depends(get_db),
                                  user: UserDB = Depends(current_active_user)):
    try:
        return DynamicSceneQueryUsercase(db_session=db, user=user).find_specified_scenario(dynamic_scene_id)
    except:
        raise
