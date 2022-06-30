from typing import Optional, List, Any
from pydantic import BaseModel, Field


class EvaluationStandard(BaseModel):
    max_velocity_test: int = 80
    tick_max_velocity_test: int = 0
    max_average_velocity_test: int = 50
    tick_max_average_velocity_test: int = 0
    min_average_velocity_test: int = 30
    tick_min_average_velocity_test: int = 0
    max_longitudinal_accel_test: int = 5
    tick_max_longitudinal_accel_test: int = 0
    max_lateral_accel_test: int = 5
    tick_max_lateral_accel_test: int = 0
    collision_test: int = 0
    agent_block_test: int = 0
    keep_lane_test: int = 0
    off_road_test: int = 0
    on_sidewalk_test: int = 0
    wrong_lane_test: int = 0
    running_red_light_test: int = 0
    running_stop_test: int = 0


class TrafficFlow(BaseModel):
    name: str = 'traffic_flow'
    type: int = 1
    area: int = 10
    radius: int = 0
    vehicle_type: int = 1
    vehicle_create_frequency: int = 200
    vehicle_num: int = 10
    max_speed_range: int = 0
    min_speed_range: int = 200
    max_politeness: int = 0
    mix_politeness: int = 100


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
