import math

import shortuuid

from sdgApp.Application.car.usercase import split_page
from sdgApp.Application.dynamic_scenes.CommandDTOs import DynamicSceneCreateDTO, DynamicSceneUpdateDTO
from sdgApp.Application.dynamic_scenes.RespondsDTOs import DynamicSceneReadDTO
from sdgApp.Domain.dynamic_scenes.dynamic_scenes import DynamicScenesAggregate
from sdgApp.Domain.dynamic_scenes.dynamic_scenes_exceptions import DynamicScenesNotFoundError
from sdgApp.Infrastructure.MongoDB.dynamic_scene.dynamic_scene_repoImpl import DynamicSceneRepoImpl
from sdgApp.Application.log.usercase import except_logger

class DynamicSceneCommandUsercase(object):

    def __init__(self, db_session, user, repo=DynamicSceneRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    @except_logger("DynamicScene create_scenario failed .....................")
    async def create_scenario(self, dynamic_scene_create_model: DynamicSceneCreateDTO):
        try:
            uuid = shortuuid.uuid()
            scenario = DynamicScenesAggregate(
                uuid,
                name=dynamic_scene_create_model.name,
                desc=dynamic_scene_create_model.desc,
                scene_script=dynamic_scene_create_model.scene_script,
                type=dynamic_scene_create_model.type)
            await self.repo.create_scenario(scenario)
        except:
            raise
    @except_logger("DynamicScene delete_scenario failed .....................")
    async def delete_scenario(self, dynamic_scene_id: str):
        try:
            await self.repo.delete_scenario_by_id(dynamic_scene_id)
        except:
            raise
    @except_logger("DynamicScene update_scenario failed .....................")
    async def update_scenario(self, dynamic_scene_id: str, dynamic_scene_update_model: DynamicSceneUpdateDTO):
        try:
            scenario_retrieved = await self.repo.get(dynamic_scene_id)
            scenario_retrieved.name = dynamic_scene_update_model.name
            scenario_retrieved.desc = dynamic_scene_update_model.desc
            scenario_retrieved.scene_script = dynamic_scene_update_model.scene_script
            scenario_retrieved.type = dynamic_scene_update_model.type
            await self.repo.update_scenario(dynamic_scene_id, scenario_retrieved)
        except:
            raise


class DynamicSceneQueryUsercase(object):

    def __init__(self, db_session, user):
        self.user = user
        self.db_session = db_session
        self.scenarios_collection = self.db_session['dynamic_scenes']
    @except_logger("DynamicScene find_specified_scenario failed .....................")
    async def find_specified_scenario(self, dynamic_scene_id: str):
        try:
            filter = {'id': dynamic_scene_id}
            filter.update({"usr_id": self.user.id})
            result_dict = await self.scenarios_collection.find_one(filter, {'_id': 0})
            if result_dict is None:
                raise DynamicScenesNotFoundError
            response_dto = DynamicSceneReadDTO(**result_dict)
            return response_dto
        except:
            raise
    @except_logger("DynamicScene find_all_scenarios failed .....................")
    async def find_all_scenarios(self, p_num, p_size, content):
        try:
            filter = {}
            filter.update({"usr_id": self.user.id})
            if content not in [""]:
                filter.update({"$or": [{"name": {"$regex": content, "$options": "$i"}},
                                       {"desc": {"$regex": content, "$options": "$i"}}]})
            total_num = await self.scenarios_collection.count_documents(filter)
            total_page_num = math.ceil(total_num / p_size)
            if p_num > total_page_num and total_page_num > 0:
                p_num = total_page_num
            if p_num > 0:
                results_dict = self.scenarios_collection.find(filter, {'_id': 0}).sort([('last_modified', -1)]).skip((p_num-1) * p_size).limit(p_size).to_list(length=50)
            else:
                results_dict = self.scenarios_collection.find(filter, {'_id': 0}).sort([('last_modified', -1)]).to_list(length=total_num)
            if results_dict:
                response_dic = {}
                response_dto_lst = []
                response_dic["total_num"] = total_num
                response_dic["total_page_num"] = total_page_num

                for doc in await results_dict:
                    response_dto_lst.append(DynamicSceneReadDTO(**doc))
                response_dic["datas"] = response_dto_lst
                return response_dic
        except:
            raise

