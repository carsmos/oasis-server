from sdgApp.Application.scenarios.RespondsDTOs import ScenariosReadDTO
from sdgApp.Application.scenarios.CommandDTOs import ScenarioCreateDTO, ScenarioUpdateDTO
from sdgApp.Application.scenarios.usercase import ScenarioCommandUsercase, ScenarioQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from fastapi import APIRouter, status, Depends
from typing import List

router = APIRouter()


@router.post(
    "/scenarios",
    status_code=status.HTTP_201_CREATED,
    response_model=ScenariosReadDTO,
    tags=["Scenarios"]
)
async def create_scenario(scenario_create_model: ScenarioCreateDTO, db=Depends(get_db)):
    try:
        result = ScenarioCommandUsercase(db_session=db).create_scenario(scenario_create_model)
        if result:
            return await find_specified_scenario(result, db)
    except:
        raise


@router.delete("/scenarios/{scenario_id}", tags=["Scenarios"])
async def delete_scenario(scenario_id: str, db=Depends(get_db)):
    try:
        return ScenarioCommandUsercase(db_session=db).delete_scenario(scenario_id)
    except:
        raise


@router.put(
    "/scenarios/{scenario_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ScenariosReadDTO,
    tags=["Scenarios"]
)
async def update_scenario(scenario_id: str,
                          scenario_update_model: ScenarioUpdateDTO,
                          db=Depends(get_db)):
    try:
        result = ScenarioCommandUsercase(db_session=db).update_scenario(scenario_id,
                                                                     scenario_update_model)
        if result:
            return await find_specified_scenario(scenario_id, db)
    except:
        raise


@router.get(
    "/scenarios",
    status_code=status.HTTP_200_OK,
    response_model=List[ScenariosReadDTO],
    tags=["Scenarios"]
)
async def find_all_scenarios(db=Depends(get_db)):
    try:
        return ScenarioQueryUsercase(db_session=db).find_all_scenarios()
    except:
        raise


@router.get(
    "/scenarios/{scenario_id}",
    status_code=status.HTTP_200_OK,
    response_model=ScenariosReadDTO,
    tags=["Scenarios"]
)
async def find_specified_scenario(scenario_id: str, db=Depends(get_db)):
    try:
        return ScenarioQueryUsercase(db_session=db).find_specified_scenario(scenario_id)
    except:
        raise
