from typing import Optional, List, Any
from pydantic import BaseModel, Field


class EvaluationStandard(BaseModel):
    max_velocity_test: int = 80
    tick_max_velocity_test: bool = True
    # max_average_velocity_test: int = 50
    # tick_max_average_velocity_test: bool = True
    min_average_velocity_test: int = 30
    tick_min_average_velocity_test: bool = True
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
    name: str = 'traffic_flow'
    # 0：车辆，1：行人
    type: int = 0
    # 0：主车周围，1：全范围
    area: int = 1
    radius: int = 0
    vehicle_type: Optional[List[str]] = None
    # 0: 每分钟，1：每百米
    vehicle_create_frequency: int = 0
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
    traffic_flow: Optional[List[TrafficFlow]]
