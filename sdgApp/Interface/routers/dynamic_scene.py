from sdgApp.Application.dynamic_scenes.RespondsDTOs import ScenarioReadDTO
from sdgApp.Application.dynamic_scenes.CommandDTOs import ScenarioCreateDTO, ScenarioUpdateDTO
from sdgApp.Application.dynamic_scenes.usercase import ScenarioCommandUsercase, \
    ScenarioDeleteUsercase, ScenarioUpdateUsercase, ScenarioQueryUsercase
from fastapi import APIRouter, status
from typing import List

router = APIRouter()


@router.post(
    "/dynamic_scenes",
    status_code=status.HTTP_201_CREATED,
    response_model=ScenarioReadDTO,
    tags=["DynamicScenes"]
)
async def create_dynamic_scene(dynamic_scene_create_model: ScenarioCreateDTO):
    try:
        return ScenarioCommandUsercase().create_scenario(dynamic_scene_create_model)
    except:
        raise


@router.delete("/dynamic_scenes/{dynamic_scene_id}", tags=["DynamicScenes"])
async def delete_dynamic_scene(dynamic_scene_id: str):
    try:
        return ScenarioDeleteUsercase().delete_scenario(dynamic_scene_id)
    except:
        raise


@router.put(
    "/dynamic_scenes/{dynamic_scene_id}",
    response_model=ScenarioReadDTO,
    tags=["DynamicScenes"]
)
async def update_dynamic_scene(dynamic_scene_id: str,
                               dynamic_scene_id_update_model: ScenarioUpdateDTO):
    try:
        return ScenarioUpdateUsercase().update_scenario(dynamic_scene_id, dynamic_scene_id_update_model)
    except:
        raise


@router.get(
    "/dynamic_scenes",
    status_code=status.HTTP_200_OK,
    response_model=List[ScenarioReadDTO],
    tags=["DynamicScenes"]
)
async def find_all_dynamic_scenes():
    try:
        return ScenarioQueryUsercase().find_all_scenarios()
    except:
        raise


@router.get(
    "/dynamic_scenes/{dynamic_scene_id}",
    status_code=status.HTTP_200_OK,
    response_model=ScenarioReadDTO,
    tags=["DynamicScenes"]
)
async def find_specified_scenario(dynamic_scene_id: str):
    try:
        return ScenarioQueryUsercase().find_specified_scenario(dynamic_scene_id)
    except:
        raise
