import math
import os
from datetime import datetime

import shortuuid

from sdgApp.Application.log.usercase import except_logger
from sdgApp.Application.scenarios.RespondsDTOs import ScenariosReadDTO, ScenarioGroupReadDTO
from sdgApp.Application.scenarios.CommandDTOs import ScenarioCreateDTO, ScenarioUpdateDTO
from sdgApp.Application.scenarios.utils import scenarios_to_tree, file_child_ids_in_scenarios
from sdgApp.Domain.scenarios.scenarios import ScenariosAggregate
from sdgApp.Domain.scenarios.scenarios_exceptions import ScenarioNotFoundError
from sdgApp.Infrastructure.MongoDB.scenario.scenario_DO import TrafficFLowBlueprintDO
from sdgApp.Infrastructure.MongoDB.scenario.scenario_repoImpl import ScenarioRepoImpl


class ScenarioCommandUsercase(object):

    def __init__(self, db_session, user, repo=ScenarioRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    @except_logger("Scenario create_scenario failed .....................")
    async def create_scenario(self, scenario_create_model: ScenarioCreateDTO):
        try:
            uuid = shortuuid.uuid()
            scenario = ScenariosAggregate(uuid,
                                          name=scenario_create_model.name,
                                          desc=scenario_create_model.desc,
                                          tags=scenario_create_model.tags,
                                          types=scenario_create_model.types,
                                          parent_id=scenario_create_model.parent_id,
                                          scenario_param=scenario_create_model.scenario_param
                                          )
            scenario = await self.repo.create_scenario(scenario)
            return ScenariosReadDTO(**scenario)
        except:
            raise

    @except_logger("Scenario delete_scenario failed .....................")
    async def delete_scenario(self, scenario_id: str):
        try:
            await self.repo.delete_scenario_by_id(scenario_id)
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
            scenario_retrieved.types = scenario_update_model.types
            scenario_retrieved.parent_id = scenario_update_model.parent_id
            scenario = await self.repo.update_scenario(scenario_id, scenario_retrieved)
            return ScenariosReadDTO(**scenario)
        except:
            raise


class ScenarioQueryUsercase(object):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.scenarios_collection = self.db_session['scenarios']
        self.traffic_flow_blueprint_collection = self.db_session['traffic_flow_blueprint']
        self.user = user

    @except_logger("Scenario find_specified_scenario failed .....................")
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
            filter = {}
            if keyword:
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
########################################### scenario-group part ##########################################

class ScenarioGroupCommandUsercase(object):

    def __init__(self, db_session, user, repo=ScenarioRepoImpl):
        self.db = db_session
        self.user = user
        self.repo = repo
        self.repo = self.repo(db_session, user)
        self.scenarios_collection = db_session['scenarios']

    async def add_scenario_group_dir(self, parent_id, name, current_id):
        try:
            uuid = shortuuid.uuid()
            scenario = ScenariosAggregate(uuid,
                                          name=name,
                                          desc="",
                                          tags=[],
                                          types="dir",
                                          parent_id=parent_id,
                                          scenario_param={}
                                          )
            await self.repo.create_scenario(scenario)
            return await ScenarioGroupQueryUsercase(db_session=self.db, user=self.user).show_scenario_group(current_id)
        except:
            raise

    async def rename_scenario_group_dir(self, scenario_id, new_name):
        try:
            filter = {'id': scenario_id}
            filter.update({"usr_id": self.user.id})
            await self.scenarios_collection.update_one(filter, {'$set': {"name": new_name,
                                                "last_modified": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}})
            return {"new_name": new_name}
        except:
            raise

    async def add_scenario_group_dir_tags(self, scenario_id, tags):
        try:
            filter = {'id': scenario_id}
            filter.update({"usr_id": self.user.id})
            tags = tags.split('+')
            scenario_retrieved = await self.repo.get(scenario_id)
            scenario_tags = scenario_retrieved.tags
            scenario_tags.extend(tags)
            scenario_tags = list(set(scenario_tags))
            await self.scenarios_collection.update_one(filter, {'$set': {"tags": scenario_tags,
                                                "last_modified": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}})
            scenario = await self.scenarios_collection.find_one(filter)
            return ScenariosReadDTO(**scenario)
        except:
            raise

    async def delete_scenario_group_dir(self, scenario_id, current_id):
        try:
            filter = {"usr_id": self.user.id}
            total_num = await self.scenarios_collection.count_documents(filter)
            scenarios = await self.scenarios_collection.find(filter).to_list(length=total_num)
            await delete_scenario_group(scenario_id, scenarios, self.repo)
            trees = await ScenarioGroupQueryUsercase(db_session=self.db, user=self.user).get_scenario_group_tree()
            shows = await ScenarioGroupQueryUsercase(db_session=self.db, user=self.user).show_scenario_group(current_id)
            return {"trees": trees, "shows": shows}
        except:
            raise

    async def delete_scenario_group_select(self, select_ids, current_id):
        try:
            filter = {"usr_id": self.user.id}
            total_num = await self.scenarios_collection.count_documents(filter)
            scenarios = await self.scenarios_collection.find(filter).to_list(length=total_num)
            select_ids = select_ids.split("+")
            for select_id in select_ids:
                await delete_scenario_group(select_id, scenarios, self.repo)
            trees = await ScenarioGroupQueryUsercase(db_session=self.db, user=self.user).get_scenario_group_tree()
            shows = await ScenarioGroupQueryUsercase(db_session=self.db, user=self.user).show_scenario_group(current_id)
            return {"trees": trees, "shows": shows}
        except:
            raise

    async def move_scenario_group_select(self, select_ids, target_id, current_id):
        try:
            select_ids = select_ids.split("+")
            for select_id in select_ids:
                filter = {'id': select_id, "usr_id": self.user.id}
                await self.scenarios_collection.update_one(filter, {'$set': {"parent_id": target_id}})
            trees = await ScenarioGroupQueryUsercase(db_session=self.db, user=self.user).get_scenario_group_tree()
            shows = await ScenarioGroupQueryUsercase(db_session=self.db, user=self.user).show_scenario_group(current_id)
            return {"trees": trees, "shows": shows}
        except:
            raise


class ScenarioGroupQueryUsercase(object):
    def __init__(self, db_session, user):
        self.db_session = db_session
        self.scenarios_collection = self.db_session['scenarios']
        self.user = user

    async def get_scenario_group_tree(self):
        try:
            filter = {"usr_id": self.user.id}
            total_num = await self.scenarios_collection.count_documents(filter)
            scenarios = await self.scenarios_collection.find(filter).to_list(length=total_num)
            trees = scenarios_to_tree("root", "root", "dir", [], scenarios, 0)
            if trees:
                return trees
            else:
                return {}
        except:
            raise

    async def show_scenario_group(self, parent_id):
        try:
            filter = {"usr_id": self.user.id, "parent_id": parent_id}
            total_num = await self.scenarios_collection.count_documents(filter)
            scenarios = await self.scenarios_collection.find(filter).sort([('types', -1)]).to_list(length=total_num)
            if scenarios:
                response_scenarios = []
                for scenario in scenarios:
                    response_scenarios.append(ScenarioGroupReadDTO(**scenario))
                return response_scenarios
            else:
                return []
        except:
            raise

    async def search_scenario_group(self, parent_id, content):
        try:
            filter = {"usr_id": self.user.id}
            total_num = await self.scenarios_collection.count_documents(filter)
            scenarios = await self.scenarios_collection.find(filter).to_list(length=total_num)
            file_child_ids = file_child_ids_in_scenarios(parent_id, scenarios)
            filter.update({"id": {"$in": file_child_ids}})
            if content:
                filter.update({"$or": [{"name": {"$regex": content, "$options": "$i"}},
                                       {"desc": {"$regex": content, "$options": "$i"}},
                                       {"tags": {"$regex": content, "$options": "$i"}}]
                               })
            scenarios_searchs = await self.scenarios_collection.find(filter).to_list(length=100)
            if scenarios_searchs:
                scenarios_response = []
                for scenarios_search in scenarios_searchs:
                    scenarios_response.append(ScenarioGroupReadDTO(**scenarios_search))
                return scenarios_response
            else:
                return {}
        except:
            raise
