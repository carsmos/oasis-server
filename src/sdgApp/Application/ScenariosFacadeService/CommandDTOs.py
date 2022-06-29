from typing import Optional, List, Any
from pydantic import BaseModel, Field


class EvaluationStandard(BaseModel):
    max_velocity_test: int
    tick_max_velocity_test: int
    max_average_velocity_test: int
    tick_max_average_velocity_test: int
    min_average_velocity_test: int
    tick_min_average_velocity_test: int
    max_longitudinal_accel_test: int
    tick_max_longitudinal_accel_test: int
    max_lateral_accel_test: int
    tick_max_lateral_accel_test: int
    collision_test: int
    agent_block_test: int
    keep_lane_test: int
    off_road_test: int
    on_sidewalk_test: int
    wrong_lane_test: int
    running_red_light_test: int
    running_stop_test: int


class TrafficFlow(BaseModel):
    name: str
    type: int
    area: int
    radius: int
    vehicle_type: int
    vehicle_create_frequency: int
    vehicle_num: int
    max_speed_range: int
    min_speed_range: int
    max_politeness: int
    mix_politeness: int


class AssemberScenarioCreateDTO(BaseModel):
    id: Optional[str]
    name: str = Field(..., example="scenario_01")
    desc: Optional[str] = Field(None, example="This is a demo scenario")
    map_name: str = Field(..., example="Town01")
    dynamic_scene_id: str = Field(..., example="e4aKGHrRpM2tBVyVppdYSq")
    weather_id: str = Field(None, example="e4aKGHrRpM2tBVyVppdYSq")
    light_id: str = Field(None, example="e4aKGHrRpM2tBVyVppdYSq")
    tags: Optional[list] = Field([], example=['tag1', 'tag2'])
    types: str = Field(..., example="file")
    parent_id: Any = Field(..., example="root")
    evaluation_standard: EvaluationStandard
    traffic_flow: List[TrafficFlow]
