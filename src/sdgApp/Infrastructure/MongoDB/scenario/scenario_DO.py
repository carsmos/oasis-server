from pydantic import BaseModel
from pydantic.typing import Any

from Application.ScenariosFacadeService.CommandDTOs import EvaluationStandard, TrafficFlow
from sdgApp.Domain.scenarios.scenarios import ScenariosAggregate


class ScenarioDO(BaseModel):
    id: str
    name: str
    desc: str
    scenario_param: dict
    usr_id: Any
    tags: Any
    create_time: str = None
    last_modified: str

    def to_entity(self) -> ScenariosAggregate:
        return ScenariosAggregate(
            id=self.id,
            name=self.name,
            desc=self.desc,
            tags=self.tags,
            scenario_param=self.scenario_param
        )


class EvaluationStandardDO(BaseModel):
    id: str = None
    scenario_id: str = None
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
    create_time: str = None
    last_modified: str

    def to_entity(self) -> EvaluationStandard:
        return EvaluationStandard(
            id=self.id,
            scenario_id=self.scenario_id,
            max_velocity_test=self.max_velocity_test,
            tick_max_velocity_test=self.tick_max_velocity_test,
            max_average_velocity_test=self.max_average_velocity_test,
            tick_max_average_velocity_test=self.tick_max_average_velocity_test,
            min_average_velocity_test=self.min_average_velocity_test,
            tick_min_average_velocity_test=self.tick_min_average_velocity_test,
            max_longitudinal_accel_test=self.max_longitudinal_accel_test,
            tick_max_longitudinal_accel_test=self.tick_max_longitudinal_accel_test,
            max_lateral_accel_test=self.max_lateral_accel_test,
            tick_max_lateral_accel_test=self.tick_max_lateral_accel_test,
            collision_test=self.collision_test,
            agent_block_test=self.agent_block_test,
            keep_lane_test=self.keep_lane_test,
            off_road_test=self.off_road_test,
            on_sidewalk_test=self.on_sidewalk_test,
            wrong_lane_test=self.wrong_lane_test,
            running_red_light_test=self.running_red_light_test,
            running_stop_test=self.running_stop_test
        )


class TrafficFlowDO(BaseModel):
    id: str = None
    scenario_id: str = None
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
    create_time: str = None
    last_modified: str

    def to_entity(self) -> TrafficFlow:
        return TrafficFlow(
            id=self.id,
            scenario_id=self.scenario_id,
            name=self.name,
            type=self.type,
            area=self.area,
            radius=self.radius,
            vehicle_type=self.vehicle_type,
            vehicle_create_frequency=self.vehicle_create_frequency,
            vehicle_num=self.vehicle_num,
            max_speed_range=self.max_speed_range,
            min_speed_range=self.min_speed_range,
            max_politeness=self.max_politeness,
            mix_politeness=self.mix_politeness
        )

