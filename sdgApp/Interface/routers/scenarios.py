from sdgApp.Application.scenarios.RespondsDTOs import ScenariosReadDTO
from sdgApp.Application.scenarios.CommandDTOs import ScenarioCreateDTO, ScenarioUpdateDTO
from sdgApp.Application.scenarios.usercase import ScenarioCommandUsercase, \
    ScenarioDeleteUsercase, ScenarioUpdateUsercase, ScenarioQueryUsercase
from fastapi import APIRouter, status
from typing import List

router = APIRouter()


@router.post(
    "/scenarios",
    status_code=status.HTTP_201_CREATED,
    response_model=ScenariosReadDTO,
    tags=["Scenarios"]
)
async def create_scenario(scenario_create_model: ScenarioCreateDTO):
    try:
        return ScenarioCommandUsercase().create_scenario(scenario_create_model)
    except:
        raise


@router.delete("/scenarios/{scenario_id}", tags=["Scenarios"])
async def delete_scenario(scenario_id: str):
    try:
        return ScenarioDeleteUsercase().delete_scenario(scenario_id)
    except:
        raise


@router.put(
    "/scenarios/{scenario_id}",
    response_model=ScenariosReadDTO,
    tags=["Scenarios"]
)
async def update_scenario(scenario_id: str,
                          scenario_update_model: ScenarioUpdateDTO):
    try:
        return ScenarioUpdateUsercase().update_scenario(scenario_id, scenario_update_model)
    except:
        raise


@router.get(
    "/scenarios",
    status_code=status.HTTP_200_OK,
    response_model=List[ScenariosReadDTO],
    tags=["Scenarios"]
)
async def find_all_scenarios():
    try:
        return ScenarioQueryUsercase().find_all_scenarios()
    except:
        raise


@router.get(
    "/scenarios/{scenario_id}",
    status_code=status.HTTP_200_OK,
    response_model=ScenariosReadDTO,
    tags=["Scenarios"]
)
async def find_specified_scenario(scenario_id: str):
    try:
        return ScenarioQueryUsercase().find_specified_scenario(scenario_id)
    except:
        raise
