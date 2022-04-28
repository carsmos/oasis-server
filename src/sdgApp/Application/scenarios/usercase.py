import copy
import math

import shortuuid
from sdgApp.Application.scenarios.RespondsDTOs import ScenariosReadDTO
from sdgApp.Application.scenarios.CommandDTOs import ScenarioCreateDTO, ScenarioUpdateDTO
from sdgApp.Domain.scenarios.scenarios import ScenariosAggregate
from sdgApp.Domain.scenarios.scenarios_exceptions import ScenarioNotFoundError
from sdgApp.Infrastructure.MongoDB.scenario.scenario_repoImpl import ScenarioRepoImpl


class ScenarioCommandUsercase(object):

    def __init__(self, db_session, user, repo=ScenarioRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    async def create_scenario(self, scenario_create_model: ScenarioCreateDTO):
        try:
            uuid = shortuuid.uuid()
            scenario = ScenariosAggregate(uuid,
                                          name=scenario_create_model.name,
                                          desc=scenario_create_model.desc,
                                          tags=scenario_create_model.tags,
                                          scenario_param=scenario_create_model.scenario_param
                                          )
            await self.repo.create_scenario(scenario)
        except:
            raise

    async def delete_scenario(self, scenario_id: str):
        try:
            await self.repo.delete_scenario_by_id(scenario_id)
        except:
            raise

    async def update_scenario(self, scenario_id: str, scenario_update_model: ScenarioUpdateDTO):
        try:
            scenario_retrieved = await self.repo.get(scenario_id)
            scenario_retrieved.name = scenario_update_model.name
            scenario_retrieved.desc = scenario_update_model.desc
            scenario_retrieved.tags = scenario_update_model.tags
            scenario_retrieved.scenario_param = scenario_update_model.scenario_param
            await self.repo.update_scenario(scenario_id, scenario_retrieved)
        except:
            raise


class ScenarioQueryUsercase(object):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.scenarios_collection = self.db_session['scenarios']
        self.user = user

    async def find_specified_scenario(self, scenario_id: str):
        try:
            filter = {"id": scenario_id}
            filter.update({"usr_id": self.user.id})
            result_dict = await self.scenarios_collection.find_one(filter)
            if result_dict is None:
                raise ScenarioNotFoundError
            return ScenariosReadDTO(**result_dict)
        except:
            raise

    async def find_all_scenarios(self, p_num, limit: int = 15):
        try:
            filter = {}
            filter.update({"usr_id": self.user.id})
            total_num = await self.scenarios_collection.count_documents(filter)
            total_page_num = math.ceil(total_num / limit)
            if p_num > total_page_num and total_page_num > 0:
                p_num = total_page_num
            if p_num > 0:
                results_dict = self.scenarios_collection.find(filter).sort([('last_modified', -1)]).skip((p_num-1) * limit).limit(limit).to_list(length=50)
            else:
                results_dict = self.scenarios_collection.find(filter).sort([('last_modified', -1)]).to_list(length=total_num)
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

    async def find_scenarios_by_tags(self, tags, p_num, limit: int = 15):
        try:
            filter = {}
            tag_list = tags.split("+")
            tag_list.append(copy.deepcopy(tag_list)) if len(tag_list) > 1 else tag_list
            tar_list = tags.split("+")[::-1]
            tar_list.append(tags.split("+")[::-1]) if len(tar_list) > 1 else tar_list
            filter.update({"usr_id": self.user.id, "$or": [{"tags": {"$all": tag_list}}, {"tags": {"$all": tar_list}}]})
            total_num = await self.scenarios_collection.count_documents(filter)
            total_page_num = math.ceil(total_num / limit)
            if p_num > total_page_num and total_page_num > 0:
                p_num = total_page_num
            results_dict = self.scenarios_collection.find(filter).sort([('last_modified', -1)]).skip((p_num-1) * limit).limit(limit).to_list(length=50)
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