from datetime import datetime
from typing import List

import shortuuid

from sdgApp.Application.ScenariosFacadeService.CommandDTOs import TrafficFlow
from sdgApp.Domain.scenarios.traffic_flow_repo import TrafficFlowRepo
from sdgApp.Infrastructure.MongoDB.scenario.scenario_DO import TrafficFlowDO


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    pass


class TrafficFLowImpl(TrafficFlowRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.traffic_flow_collection = self.db_session['traffic_flow']

    async def create_traffic_flow(self, scenario_id: str, traffic_flow: TrafficFlow):
        traffic_flow_DO = TrafficFlowDO(id=shortuuid.uuid(),
                                        scenario_id=scenario_id,
                                        name=traffic_flow.name,
                                        type=traffic_flow.type,
                                        area=traffic_flow.area,
                                        radius=traffic_flow.radius,
                                        vehicle_type=traffic_flow.vehicle_type,
                                        vehicle_create_frequency=traffic_flow.vehicle_create_frequency,
                                        vehicle_num=traffic_flow.vehicle_num,
                                        max_speed_range=traffic_flow.max_speed_range,
                                        min_speed_range=traffic_flow.min_speed_range,
                                        max_politeness=traffic_flow.max_politeness,
                                        mix_politeness=traffic_flow.mix_politeness,
                                        create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                        last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        )
        traffic_flow = await self.traffic_flow_collection.insert_one(traffic_flow_DO.dict())
        if traffic_flow:
            return traffic_flow_DO.dict()

    async def create_traffic_flow_list(self, scenario_id: str, traffic_flow_list: List[TrafficFlow]):
        traffic_flow_DO_list = []
        for traffic_flow in traffic_flow_list:
            traffic_flow_DO = TrafficFlowDO(id=traffic_flow.id if traffic_flow.id else shortuuid.uuid(),
                                            scenario_id=scenario_id,
                                            name=traffic_flow.name,
                                            type=traffic_flow.type,
                                            area=traffic_flow.area,
                                            radius=traffic_flow.radius,
                                            vehicle_type=traffic_flow.vehicle_type,
                                            vehicle_create_frequency=traffic_flow.vehicle_create_frequency,
                                            vehicle_num=traffic_flow.vehicle_num,
                                            max_speed_range=traffic_flow.max_speed_range,
                                            min_speed_range=traffic_flow.min_speed_range,
                                            max_politeness=traffic_flow.max_politeness,
                                            mix_politeness=traffic_flow.mix_politeness,
                                            create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                            last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            )
            traffic_flow_DO_list.append(traffic_flow_DO.dict())

        traffic_flow = await self.traffic_flow_collection.insert_many(traffic_flow_DO_list)
        if traffic_flow:
            return traffic_flow_DO_list

    async def delete_traffic_flow_by_id(self, traffic_id: str):
        filter = {"id": traffic_id}
        await self.traffic_flow_collection.delete_one(filter)

    async def delete_traffic_flow_by_scenario_id(self, scenario_id: str):
        filter = {"scenario_id": scenario_id}
        await self.traffic_flow_collection.delete_many(filter)

    async def update_traffic_flow(self, traffic_id: str, traffic_flow: TrafficFlow):
        traffic_flow_DO = TrafficFlowDO(id=shortuuid.uuid(),
                                        scenario_id=None,
                                        name=traffic_flow.name,
                                        type=traffic_flow.type,
                                        area=traffic_flow.area,
                                        radius=traffic_flow.radius,
                                        vehicle_type=traffic_flow.vehicle_type,
                                        vehicle_create_frequency=traffic_flow.vehicle_create_frequency,
                                        vehicle_num=traffic_flow.vehicle_num,
                                        max_speed_range=traffic_flow.max_speed_range,
                                        min_speed_range=traffic_flow.min_speed_range,
                                        max_politeness=traffic_flow.max_politeness,
                                        mix_politeness=traffic_flow.mix_politeness,
                                        create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                        last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        )
        filter = {'id': traffic_id}
        filter.update({"usr_id": self.user.id})
        await self.traffic_flow_collection.update_one(filter, {
            '$set': traffic_flow_DO.dict(exclude={'id', 'scenario_id', 'create_time'})})
        return traffic_flow_DO.dict()

    async def update_traffic_flow_list(self, scenario_id: str, traffic_flow_list: List[TrafficFlow]):
        await self.delete_traffic_flow_by_scenario_id(scenario_id)
        return await self.create_traffic_flow_list(scenario_id, traffic_flow_list)

    async def get(self, traffic_id: str):
        filter = {'id': traffic_id}
        result_dict = await self.traffic_flow_collection.find_one(filter)
        if result_dict:
            traffic_flow_DO = TrafficFlowDO(**result_dict).to_entity()
            return traffic_flow_DO

    async def list(self, scenario_id: str):
        filter = {'scenario_id': scenario_id}
        one_traffic_flow_list = []
        results_dict = self.traffic_flow_collection.find(filter)
        if results_dict:
            async for one_result in results_dict:
                one_traffic_flow = TrafficFlowDO(**one_result).to_entity()
                one_traffic_flow_list.append(one_traffic_flow.dict())
            return one_traffic_flow_list
