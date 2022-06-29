import copy
import math
import os
from datetime import datetime

import shortuuid

from sdgApp.Infrastructure.MongoDB.scenario.evaluation_standard_repoImpl import EvaluationStandardImpl
from sdgApp.Infrastructure.MongoDB.scenario.scenario_DO import TrafficFLowBlueprintDO
from sdgApp.Infrastructure.MongoDB.scenario.traffic_flow_repoImpl import TrafficFLowImpl
from sdgApp.Application.scenarios.RespondsDTOs import ScenariosReadDTO
from sdgApp.Application.scenarios.CommandDTOs import ScenarioCreateDTO, ScenarioUpdateDTO, TrafficFLowBlueprintDTO
from sdgApp.Domain.scenarios.scenarios import ScenariosAggregate
from sdgApp.Domain.scenarios.scenarios_exceptions import ScenarioNotFoundError
from sdgApp.Infrastructure.MongoDB.scenario.scenario_repoImpl import ScenarioRepoImpl
from sdgApp.Application.log.usercase import except_logger


class ScenarioCommandUsercase(object):

    def __init__(self, db_session, user, repo=ScenarioRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)
        self.traffic_repo = TrafficFLowImpl(db_session, user)
        self.evaluation_repo = EvaluationStandardImpl(db_session, user)

    @except_logger("Scenario create_scenario failed .....................")
    async def create_scenario(self, scenario_create_model: ScenarioCreateDTO):
        try:
            uuid = shortuuid.uuid()
            scenario = ScenariosAggregate(uuid,
                                          name=scenario_create_model.name,
                                          desc=scenario_create_model.desc,
                                          tags=scenario_create_model.tags,
                                          scenario_param=scenario_create_model.scenario_param
                                          )
            scenario = await self.repo.create_scenario(scenario)
            evaluation_standard = await self.evaluation_repo.create_evaluation_standard(uuid, scenario_create_model.evaluation_standard)
            traffic_flow = await self.traffic_repo.create_traffic_flow_list(uuid, scenario_create_model.traffic_flow)
            if scenario:
                scenario.setdefault("traffic_flow", traffic_flow)
                scenario.setdefault("evaluation_standard", evaluation_standard)
                return ScenariosReadDTO(**scenario)
        except:
            raise

    @except_logger("Scenario delete_scenario failed .....................")
    async def delete_scenario(self, scenario_id: str):
        try:
            await self.repo.delete_scenario_by_id(scenario_id)
            await self.traffic_repo.delete_traffic_flow_by_scenario_id(scenario_id)
            await self.evaluation_repo.delete_evaluation_standard_by_scenario_id(scenario_id)
        except:
            raise

    @except_logger("Scenario update_scenario failed .....................")
    async def update_scenario(self, scenario_id: str, scenario_update_model: ScenarioUpdateDTO):
        try:
            scenario_retrieved = await self.repo.get(scenario_id)
            scenario_retrieved.name = scenario_update_model.name
            scenario_retrieved.desc = scenario_update_model.desc
            scenario_retrieved.tags = scenario_update_model.tags
            scenario_retrieved.scenario_param = scenario_update_model.scenario_param
            scenario = await self.repo.update_scenario(scenario_id, scenario_retrieved)
            traffic_flow = await self.traffic_repo.update_traffic_flow_list(scenario_id, scenario_update_model.traffic_flow)
            evaluation_standard = await self.evaluation_repo.update_evaluation_standard(scenario_update_model.evaluation_standard)
            if scenario:
                scenario.update({"create_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
                scenario.setdefault("traffic_flow", traffic_flow)
                scenario.setdefault("evaluation_standard", evaluation_standard)
                return ScenariosReadDTO(**scenario)
        except:
            raise


class ScenarioQueryUsercase(object):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.scenarios_collection = self.db_session['scenarios']
        self.traffic_flow_blueprint_collection = self.db_session['traffic_flow_blueprint']
        self.traffic_repo = TrafficFLowImpl(db_session, user)
        self.evaluation_repo = EvaluationStandardImpl(db_session, user)
        self.user = user

    @except_logger("Scenario find_specified_scenario failed .....................")
    async def find_specified_scenario(self, scenario_id: str):
        try:
            filter = {"id": scenario_id}
            filter.update({"usr_id": self.user.id})
            result_dict = await self.scenarios_collection.find_one(filter)
            traffic_flow = await self.traffic_repo.list(scenario_id)
            evaluation_standard = await self.evaluation_repo.get(scenario_id)
            if result_dict is None:
                raise ScenarioNotFoundError
            result_dict.setdefault("traffic_flow", traffic_flow)
            result_dict.setdefault("evaluation_standard", evaluation_standard)
            return ScenariosReadDTO(**result_dict)
        except:
            raise

    @except_logger("Scenario find_all_scenarios failed .....................")
    async def find_all_scenarios(self, pagenum, pagesize, content, tags):
        try:
            filter = {}
            filter.update({"usr_id": self.user.id})
            if tags:
                tag_list = tags.split("+")
                filter.update({"tags": {"$all": tag_list}})
            if content:
                filter.update({"$or": [{"name": {"$regex": content, "$options": "$i"}},
                                       {"desc": {"$regex": content, "$options": "$i"}}]})
            total_num = await self.scenarios_collection.count_documents(filter)
            total_page_num = math.ceil(total_num / pagesize)
            if pagenum > total_page_num > 0:
                pagenum = total_page_num
            if pagenum > 0:
                results_dict = self.scenarios_collection.find(filter).sort([('last_modified', -1)]).skip(
                    (pagenum - 1) * pagesize).limit(pagesize).to_list(length=50)
            else:
                results_dict = self.scenarios_collection.find(filter).sort([('last_modified', -1)]).to_list(
                    length=total_num)
            if results_dict:
                response_dic = {}
                response_dto_lst = []
                response_dic["total_num"] = total_num
                response_dic["total_page_num"] = total_page_num
                for doc in await results_dict:
                    response_dto_lst.append(ScenariosReadDTO(**doc))
                response_dic["datas"] = response_dto_lst
                return response_dic
        except:
            raise

    @except_logger("Scenario find_scenarios_by_tags failed .....................")
    async def find_scenarios_by_tags(self, tags, p_num, limit: int = 15):
        try:
            filter = {}
            tag_list = tags.split("+")
            filter.update({"usr_id": self.user.id, "tags": {"$all": tag_list}})
            total_num = await self.scenarios_collection.count_documents(filter)
            total_page_num = math.ceil(total_num / limit)
            if p_num > total_page_num and total_page_num > 0:
                p_num = total_page_num
            if p_num > 0:
                results_dict = self.scenarios_collection.find(filter).sort([('last_modified', -1)]).skip(
                    (p_num - 1) * limit).limit(limit).to_list(length=50)
            else:
                results_dict = self.scenarios_collection.find(filter).sort([('last_modified', -1)]).to_list(
                    length=total_num)
            if results_dict:
                response_dic = {}
                response_dto_lst = []
                response_dic["total_num"] = total_num
                response_dic["total_page_num"] = total_page_num

                for doc in await results_dict:
                    response_dto_lst.append(ScenariosReadDTO(**doc))
                response_dic["datas"] = response_dto_lst
                return response_dic
        except:
            raise

    @except_logger("Scenario find_scenarios_by_tags failed .....................")
    async def find_traffic_flow_blueprint(self, keyword):
        try:
            filter = {"actor": {"$regex": keyword}}
            # init low_blueprint_collection
            total_num = await self.traffic_flow_blueprint_collection.count_documents({})
            if total_num == 0:
                init_list = []
                finename = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/blueprint.init")
                for line in open(finename):
                    items = line.replace('\n', '').split(":")
                    traffic_flow = TrafficFLowBlueprintDO(id=shortuuid.uuid(),
                                                          actor=items[0],
                                                          actor_class=items[1],
                                                          create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                          last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                          )
                    init_list.append(traffic_flow.dict())
                await self.traffic_flow_blueprint_collection.insert_many(init_list)

            results_dict = self.traffic_flow_blueprint_collection.find(filter)
            response_dto_lst = []
            if results_dict:
                async for one_result in results_dict:
                    one_traffic_flow = TrafficFLowBlueprintDO(**one_result).to_entity()
                    response_dto_lst.append(one_traffic_flow.dict())
                return response_dto_lst
        except:
            raise
