from typing import Optional, Any, Union, List
from pydantic import BaseModel, Field, validator
from datetime import datetime

from apps.scenario.model import Scenarios


class ScenarioCreateDTO(BaseModel):
    name: str = Field(..., example="scenario_01")
    desc: Optional[str] = Field(None, example="This is a demo scenario")
    scenario_param: Optional[dict]
    tags: Optional[list] = Field([], example=['tag1', 'tag2'])
    type: str = Field(..., example="file")
    parent_id: str = Field(..., example="root")
    is_temp: bool = False


class ScenariosReadDTO(ScenarioCreateDTO):
    id: str
    create_time: Union[None, datetime]
    last_modified: Union[None, datetime]
    type: str
    parent_id: str


class EvaluationStandard(BaseModel):
    max_velocity_test: int = 80
    tick_max_velocity_test: bool = True
    # max_average_velocity_test: int = 50
    # tick_max_average_velocity_test: bool = True
    # min_average_velocity_test: int = 30
    # tick_min_average_velocity_test: bool = True
    max_longitudinal_accel_test: int = 5
    tick_max_longitudinal_accel_test: bool = True
    max_lateral_accel_test: int = 5
    tick_max_lateral_accel_test: bool = True
    collision_test: bool = True
    agent_block_test: bool = True
    keep_lane_test: bool = True
    off_road_test: bool = True
    on_sidewalk_test: bool = True
    wrong_lane_test: bool = True
    running_red_light_test: bool = True
    running_stop_test: bool = True


class TrafficFlow(BaseModel):
    # unfold: bool
    name: str
    area: str
    radius: int
    vehicle_num: int
    vehicle_models: List[str]
    ai_traffic_flow: bool
    driving_style: str
    break_law_possibility: float
    vehicles_ratio: dict


class AssemberScenarioCreateDTO(BaseModel):
    name: str = Field(..., example="scenario_01")
    desc: Optional[str] = Field(..., example="This is a demo scenario")
    tags: Optional[list] = Field([], example=['tag1', 'tag2'])
    type: str = Field(..., example="file")
    parent_id: int = Field(..., example="root")
    is_temp: bool = False
    map_name: str = Field(..., example="scenario_01")
    # map_id: int = Field(..., example="1")
    open_scenario_json: dict = Field(..., example="{name1:value1,name2:value2}")
    ui_entities_json: dict = Field(..., example="{name1:value1,name2:value2}")
    environment: dict = Field(..., example="{weather:{},light:{}}")
    evaluation_standard: dict = Field(..., example="{name1:value1,name2:value2}")
    traffic_flow: Optional[List[TrafficFlow]]
    criterion_id: int = Field(..., example=1)


class ScenarioUpdateDTO(BaseModel):
    id: int
    name_en: str = ''
    desc_en: str = ''
    tags_en: Optional[list] = Field([], example=['tag1', 'tag2'])


class ScenarioTempCreateDTO(BaseModel):
    name: str = Field(..., example="scenario_01")
    desc: str = ''
    map_name: str = Field(..., example="scenario_01")
    # map_id: int = Field(..., example="1")
    open_scenario_json: dict = Field({}, example="{name1:value1,name2:value2}")
    ui_entities_json: dict = Field({}, example="{name1:value1,name2:value2}")
    environment: dict = Field({}, example="{weather:{},light:{}}")
    evaluation_standard: dict = Field({}, example="{name1:value1,name2:value2}")
    traffic_flow: list = Field([], example="{name1:value1,name2:value2}")
    tags: list = []
    type: str = ''
    parent_id: int = Field(example="1")
    is_temp: bool = True


class PageModel(BaseModel):
    pagenum: int = 1
    pagesize: int = 10


class SelectIds(BaseModel):
    select_ids: List[int] = Field(..., example="[1,2,3]")


class MoveScenarioGroup(SelectIds):
    parent_id: int


class AddScenarioGroupDir(BaseModel):
    name: str
    parent_id: int = None
    tags: List[str] = Field([], example="[tag1,tag2,tag3]")


class Tags(BaseModel):
    tags: List[str] = Field(..., example="[tag1,tag2,tag3]")


class ScenarioIds(BaseModel):
    scenario_ids: List[int] = Field(...)


class FindScenariosByTags(Tags, PageModel):
    pass


class AddScenarioGroupDirTags(Tags):
    scenario_id: int


class OpenScenarioJson(BaseModel):
    open_scenario_json: dict


class ShowScenarioGroup(PageModel):
    parent_id: int
    has_temp: int = 1
    tags: List[str] = Field([], example="[tag1,tag2,tag3]")


class SearchScenarioGroup(ShowScenarioGroup):
    content: str = ""


class FindAllScenarios(PageModel):
    content: str = ""
    tags: List[str] = Field([], example="[tag1,tag2,tag3]")


def scenarios_to_tree(parent_id, parent_name, type, tags, scenarios, level, system_data=0):
    childs = []
    for scenario in scenarios:
        if scenario.parent_id == parent_id:
            childs.append(scenario)

    if childs:
        total = 0
        children = []
        for child in childs:
            child_tree = scenarios_to_tree(child.id, child.name, child.type, child.tags, scenarios, level + 1,
                                           child.system_data)
            total += child_tree["total"]
            if child_tree["type"] == "dir":
                children.append(child_tree)
        if children:
            return {"id": parent_id, "name": parent_name, "type": type, "tags": tags, "level": level, "total": total,
                    "children": children, "system_data":system_data}
        else:
            return {"id": parent_id, "name": parent_name, "type": type, "tags": tags, "level": level, "total": total,
                    "system_data":system_data}
    else:
        if type == "dir":
            return {"id": parent_id, "name": parent_name, "type": type, "tags": tags, "level": level, "total": 0}
        else:
            return {"id": parent_id, "name": parent_name, "type": type, "tags": tags, "level": level, "total": 1}


def file_child_ids_in_scenarios(parent_id, scenarios):
    childs = []
    for scenario in scenarios:
        if scenario.parent_id == parent_id:
            childs.append(scenario)
    if childs:
        file_child_ids = []
        for child in childs:
            if child.type == "dir":
                child_ids = file_child_ids_in_scenarios(child.id, scenarios)
                file_child_ids.extend(child_ids)
            else:
                file_child_ids.append(child.id)
        return file_child_ids
    else:
        return []


async def delete_scenario_groups(scenario_id, scenarios):
    # childs = []
    # for scenario in scenarios:
    #     if scenario.parent_id == scenario_id:
    #         childs.append(scenario)

    for child in scenarios:
        child_scenarios = await Scenarios.filter(parent_id=child.id, invalid=0).all()
        await delete_scenario_groups(child.id, child_scenarios)

    await Scenarios.filter(id=scenario_id).update(invalid=scenario_id)
