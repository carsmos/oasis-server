from datetime import datetime

import shortuuid

from Application.ScenariosFacadeService.CommandDTOs import EvaluationStandard
from Domain.scenarios.evaluation_standard_repo import EvaluationStandardRepo
from sdgApp.Infrastructure.MongoDB.scenario.scenario_DO import EvaluationStandardDO


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    pass


class EvaluationStandardImpl(EvaluationStandardRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.evaluation_standard_collection = self.db_session['evaluation_standard']

    async def create_evaluation_standard(self, scenario_id: str, evaluation: EvaluationStandard):
        evaluation_standard_DO = EvaluationStandardDO(id=shortuuid.uuid(),
                                                      scenario_id=scenario_id,
                                                      max_velocity_test=evaluation.max_velocity_test,
                                                      tick_max_velocity_test=evaluation.tick_max_velocity_test,
                                                      max_average_velocity_test=evaluation.max_average_velocity_test,
                                                      tick_max_average_velocity_test=evaluation.tick_max_average_velocity_test,
                                                      min_average_velocity_test=evaluation.min_average_velocity_test,
                                                      tick_min_average_velocity_test=evaluation.tick_min_average_velocity_test,
                                                      max_longitudinal_accel_test=evaluation.max_longitudinal_accel_test,
                                                      tick_max_longitudinal_accel_test=evaluation.tick_max_longitudinal_accel_test,
                                                      max_lateral_accel_test=evaluation.max_lateral_accel_test,
                                                      tick_max_lateral_accel_test=evaluation.tick_max_lateral_accel_test,
                                                      collision_test=evaluation.collision_test,
                                                      agent_block_test=evaluation.agent_block_test,
                                                      keep_lane_test=evaluation.keep_lane_test,
                                                      off_road_test=evaluation.off_road_test,
                                                      on_sidewalk_test=evaluation.on_sidewalk_test,
                                                      wrong_lane_test=evaluation.wrong_lane_test,
                                                      running_red_light_test=evaluation.running_red_light_test,
                                                      running_stop_test=evaluation.running_stop_test,
                                                      create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                      last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                      )
        evaluation_standard = await self.evaluation_standard_collection.insert_one(evaluation_standard_DO.dict())
        if evaluation_standard:
            return evaluation_standard_DO.dict()

    async def delete_evaluation_standard_by_id(self, evaluation_standard_id: str):
        filter = {"id": evaluation_standard_id}
        await self.evaluation_standard_collection.delete_one(filter)

    async def delete_evaluation_standard_by_scenario_id(self, scenario_id: str):
        filter = {"scenario_id": scenario_id}
        await self.evaluation_standard_collection.delete_many(filter)

    async def update_evaluation_standard(self, evaluation: EvaluationStandard):
        evaluation_standard_DO = EvaluationStandardDO(id=evaluation.id,
                                                      scenario_id=evaluation.scenario_id,
                                                      max_velocity_test=evaluation.max_velocity_test,
                                                      tick_max_velocity_test=evaluation.tick_max_velocity_test,
                                                      max_average_velocity_test=evaluation.max_average_velocity_test,
                                                      tick_max_average_velocity_test=evaluation.tick_max_average_velocity_test,
                                                      min_average_velocity_test=evaluation.min_average_velocity_test,
                                                      tick_min_average_velocity_test=evaluation.tick_min_average_velocity_test,
                                                      max_longitudinal_accel_test=evaluation.max_longitudinal_accel_test,
                                                      tick_max_longitudinal_accel_test=evaluation.tick_max_longitudinal_accel_test,
                                                      max_lateral_accel_test=evaluation.max_lateral_accel_test,
                                                      tick_max_lateral_accel_test=evaluation.tick_max_lateral_accel_test,
                                                      collision_test=evaluation.collision_test,
                                                      agent_block_test=evaluation.agent_block_test,
                                                      keep_lane_test=evaluation.keep_lane_test,
                                                      off_road_test=evaluation.off_road_test,
                                                      on_sidewalk_test=evaluation.on_sidewalk_test,
                                                      wrong_lane_test=evaluation.wrong_lane_test,
                                                      running_red_light_test=evaluation.running_red_light_test,
                                                      running_stop_test=evaluation.running_stop_test,
                                                      create_time=None,
                                                      last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                      )
        filter = {'id': evaluation.id}
        await self.evaluation_standard_collection.update_one(filter,
                                                   {'$set': evaluation_standard_DO.dict(exclude={'id', 'scenario_id', 'create_time'})})
        return evaluation_standard_DO.dict()

    async def get(self, scenario_id: str):
        filter = {'scenario_id': scenario_id}
        result_dict = await self.evaluation_standard_collection.find_one(filter)
        if result_dict:
            evaluation = EvaluationStandardDO(**result_dict).to_entity()
            return evaluation
