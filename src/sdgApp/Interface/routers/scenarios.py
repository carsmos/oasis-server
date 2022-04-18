from sdgApp.Application.scenarios.RespondsDTOs import ScenariosReadDTO
from sdgApp.Application.scenarios.CommandDTOs import ScenarioUpdateDTO
from sdgApp.Application.scenarios.usercase import ScenarioCommandUsercase, ScenarioQueryUsercase
from sdgApp.Application.ScenariosFacadeService.CommandDTOs import AssemberScenarioCreateDTO
from sdgApp.Application.ScenariosFacadeService.AssembleService import AssembleScenarioService
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sdgApp.Interface.FastapiUsers.users_model import UserDB
from sdgApp.Interface.FastapiUsers.manager import current_active_user
from typing import List

from sdgApp.Domain.environments.envs_exceptions import EnvNotFoundError
from sdgApp.Domain.dynamic_scenes.dynamic_scenes_exceptions import DynamicScenesNotFoundError

router = APIRouter()


@router.put(
    "/scenarios-assemble",
    status_code=status.HTTP_201_CREATED,
    response_model=ScenariosReadDTO,
    tags=["Scenarios"]
)
async def create_scenario(scenario_create_model: AssemberScenarioCreateDTO,
                          db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        await AssembleScenarioService(scenario_create_model, db, user)
        AssembleScenarioService(scenario_create_model, db, user)
    except DynamicScenesNotFoundError as e:
        return JSONResponse(status_code=200, content={"status": "fail", "detail": e.message})
    except EnvNotFoundError as e:
        return JSONResponse(status_code=200, content={"status": "fail", "detail": e.message})
    except:
        raise


@router.delete("/scenarios/{scenario_id}", status_code=status.HTTP_202_ACCEPTED, tags=["Scenarios"])
async def delete_scenario(scenario_id: str, db=Depends(get_db),
                          user: UserDB = Depends(current_active_user)):
    try:
        await ScenarioCommandUsercase(db_session=db, user=user).delete_scenario(scenario_id)
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
                          db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        await ScenarioCommandUsercase(db_session=db, user=user).update_scenario(scenario_id, scenario_update_model)
    except:
        raise


@router.get(
    "/scenarios",
    status_code=status.HTTP_200_OK,
    response_model=List[ScenariosReadDTO],
    tags=["Scenarios"]
)
async def find_all_scenarios(skip: int = 0, db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioQueryUsercase(db_session=db, user=user).find_all_scenarios(skip)
    except:
        raise


@router.get(
    "/scenarios/{scenario_id}",
    status_code=status.HTTP_200_OK,
    response_model=ScenariosReadDTO,
    tags=["Scenarios"]
)
async def find_specified_scenario(scenario_id: str, db=Depends(get_db),
                                  user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioQueryUsercase(db_session=db, user=user).find_specified_scenario(scenario_id)
    except:
        raise
