from sdgApp.Application.scenarios.RespondsDTOs import ScenariosReadDTO, ScenariosResponse
from sdgApp.Application.scenarios.CommandDTOs import ScenarioUpdateDTO, TrafficFLowBlueprintDTO
from sdgApp.Application.scenarios.usercase import ScenarioCommandUsercase, ScenarioQueryUsercase
from sdgApp.Application.scenarios.CommandDTOs import ScenarioUpdateDTO
from sdgApp.Application.scenarios.usercase import ScenarioCommandUsercase, ScenarioQueryUsercase, \
    ScenarioGroupCommandUsercase, ScenarioGroupQueryUsercase
from sdgApp.Application.ScenariosFacadeService.CommandDTOs import AssemberScenarioCreateDTO
from sdgApp.Application.ScenariosFacadeService.AssembleService import AssembleScenarioService
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sdgApp.Interface.FastapiUsers.users_model import UserDB
from sdgApp.Interface.FastapiUsers.manager import current_active_user
from typing import List

from sdgApp.Domain.weather.weathers_exceptions import WeatherNotFoundError
from sdgApp.Domain.light.lights_exceptions import LightNotFoundError
from sdgApp.Domain.dynamic_scenes.dynamic_scenes_exceptions import DynamicScenesNotFoundError
from sdgApp.Application.log.usercase import except_logger
router = APIRouter()


@router.put(
    "/scenarios-assemble",
    status_code=status.HTTP_201_CREATED,
    response_model=ScenariosReadDTO,
    tags=["Scenarios"]
)
@except_logger("create_scenario failed .....................")
async def create_scenario(scenario_create_model: AssemberScenarioCreateDTO,
                          db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return await AssembleScenarioService(scenario_create_model, db, user)
    except (LightNotFoundError, WeatherNotFoundError, DynamicScenesNotFoundError) as e:
        return JSONResponse(status_code=200, content={"status": "fail", "detail": e.message})
    except:
        raise


@router.delete("/scenarios/{scenario_id}", status_code=status.HTTP_202_ACCEPTED, tags=["Scenarios"])
@except_logger("delete_scenario failed .....................")
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
@except_logger("update_scenario failed .....................")
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
    response_model=ScenariosResponse,
    tags=["Scenarios"]
)
@except_logger("find_all_scenarios failed .....................")
async def find_all_scenarios(pagenum: int = 1, pagesize: int = 10, content: str = "", tags: str = "",  db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioQueryUsercase(db_session=db, user=user).find_all_scenarios(pagenum, pagesize, content, tags)
    except:
        raise


@router.get(
    "/scenarios/{scenario_id}",
    status_code=status.HTTP_200_OK,
    response_model=ScenariosReadDTO,
    tags=["Scenarios"]
)
@except_logger("find_specified_scenario failed .....................")
async def find_specified_scenario(scenario_id: str, db=Depends(get_db),
                                  user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioQueryUsercase(db_session=db, user=user).find_specified_scenario(scenario_id)
    except:
        raise


@router.get(
    "/scenarios_by_tags",
    status_code=status.HTTP_200_OK,
    response_model=ScenariosResponse,
    tags=["Scenarios"]
)
@except_logger("find_scenarios_by_tags failed .....................")
async def find_scenarios_by_tags(tags: str, skip: int = 1,  db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioQueryUsercase(db_session=db, user=user).find_scenarios_by_tags(tags, skip)
    except:
        raise


@router.get(
    "/scenario-traffic-flow-blueprint",
    status_code=status.HTTP_200_OK,
    response_model=List[TrafficFLowBlueprintDTO],
    tags=["Scenarios"]
)
@except_logger("find_traffic_flow_blueprint failed .....................")
async def find_specified_scenario(keyword: str = None, db=Depends(get_db),
                                  user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioQueryUsercase(db_session=db, user=user).find_traffic_flow_blueprint(keyword)
    except:
        raise

########################################### scenario-group part ##########################################

### query part
# 返回当前user下全部场景树，生成左侧文件夹树，返回name， total， level
@router.get(
    "/scenario-group-tree",
    status_code=status.HTTP_200_OK,
    tags=["Scenarios"]
)
async def get_scenario_group_tree(db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioGroupQueryUsercase(db_session=db, user=user).get_scenario_group_tree()
    except:
        raise

# 根据文件夹parent_id返回场景信息，包括场景数量total，场景标签，第一级子场景名称，运行地图，标签，最后编辑时间, 按照先文件夹后文件顺序
@router.get(
    "/scenario-group-show",
    status_code=status.HTTP_200_OK,
    tags=["Scenarios"]
)
async def show_scenario_group(parent_id: str, db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioGroupQueryUsercase(db_session=db, user=user).show_scenario_group(parent_id)
    except:
        raise

# 在parent_id场景库下按照关键字搜索，
@router.get(
    "/scenario-group-search",
    status_code=status.HTTP_200_OK,
    tags=["Scenarios"]
)
async def search_scenario_group(parent_id: str, content: str, db=Depends(get_db),
                                user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioGroupQueryUsercase(db_session=db, user=user).search_scenario_group(parent_id, content)
    except:
        raise

### command part

# 场景库新建文件夹，完成后前端场景树局部更新
@router.post(
    "/scenario-group/dir-add",
    status_code=status.HTTP_201_CREATED,
    tags=["Scenarios"]
)
async def add_scenario_group_dir(parent_id: str, name: str, current_id: str,
                                 db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioGroupCommandUsercase(db_session=db, user=user).add_scenario_group_dir(parent_id, name, current_id)
    except:
        raise

# 场景库重命名文件夹， 完成后前端场景树局部更新
@router.put(
    "/scenario-group/dir-rename",
    status_code=status.HTTP_201_CREATED,
    tags=["Scenarios"]
)
async def rename_scenario_group_dir(this_id: str, new_name: str, db=Depends(get_db),
                                    user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioGroupCommandUsercase(db_session=db, user=user).rename_scenario_group_dir(this_id, new_name)
    except:
        raise

# 场景库删除文件夹，递归删除文件夹下的全部场景，完成后前端场景树全部更新返回
@router.delete(
    "/scenario-group/dir-delete",
    status_code=status.HTTP_200_OK,
    tags=["Scenarios"]
)
async def delete_scenario_group_dir(scenario_id: str, current_id: str, db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioGroupCommandUsercase(db_session=db, user=user).delete_scenario_group_dir(scenario_id, current_id)
    except:
        raise

# 场景库文件夹tags添加，成功后前端直接加入
@router.post(
    "/scenario-group/dir-tags-add",
    status_code=status.HTTP_200_OK,
    tags=["Scenarios"]
)
async def add_scenario_group_dir_tags(scenario_id: str, tags:str, db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioGroupCommandUsercase(db_session=db, user=user).add_scenario_group_dir_tags(scenario_id, tags)
    except:
        raise

# 场景库删除选中文件和文件夹， 文件夹需要递归删除，完成后前端场景树全部更新返回，同时返回右侧场景
@router.delete(
    "/scenario-group/select-delete",
    status_code=status.HTTP_200_OK,
    tags=["Scenarios"]
)
async def delete_scenario_group_select(select_ids: str, current_id: str, db=Depends(get_db),
                                       user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioGroupCommandUsercase(db_session=db, user=user).delete_scenario_group_select(select_ids, current_id)
    except:
        raise

# 场景库移动选中文件和文件夹，完成后前端场景树全部更新返回，同时返回右侧场景
@router.post(
    "/scenario-group/select-move",
    status_code=status.HTTP_200_OK,
    tags=["Scenarios"]
)
async def move_scenario_group_select(select_ids: str, target_id: str, current_id: str, db=Depends(get_db),
                                       user: UserDB = Depends(current_active_user)):
    try:
        return await ScenarioGroupCommandUsercase(db_session=db, user=user).move_scenario_group_select(select_ids, target_id, current_id)
    except:
        raise
