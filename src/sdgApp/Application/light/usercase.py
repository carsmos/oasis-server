import math

import shortuuid
from sdgApp.Application.light.RespondsDTOs import LightReadDTO
from sdgApp.Application.light.CommandDTOs import LightCreateDTO, LightUpdateDTO
from sdgApp.Domain.light.lights import LightAggregate
from sdgApp.Domain.light.lights_exceptions import LightNotFoundError
from sdgApp.Infrastructure.MongoDB.light.light_repoImpl import LightRepoImpl
from sdgApp.Application.log.usercase import except_logger


class LightCommandUsercase(object):

    def __init__(self, db_session, user, repo=LightRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    @except_logger("create_light failed .....................")
    async def create_light(self, light_create_model: LightCreateDTO):
        try:
            uuid = shortuuid.uuid()
            light = LightAggregate(id=uuid,
                                name=light_create_model.name,
                                desc=light_create_model.desc,
                                param=light_create_model.param)
            await self.repo.create_light(light)
        except:
            raise

    @except_logger("delete_light failed .....................")
    async def delete_light(self, light_ids: str):
        try:
            for light_id in light_ids.split("+"):
                await self.repo.delete_light(light_id)
        except:
            raise

    @except_logger("update_light failed .....................")
    async def update_light(self, light_id: str, light_create_model: LightUpdateDTO):
        try:
            light_retrieved = await self.repo.get(light_id)
            light_retrieved.name = light_create_model.name
            light_retrieved.desc = light_create_model.desc
            light_retrieved.param = light_create_model.param
            await self.repo.update_light(light_id, light_retrieved)
        except:
            raise


class LightQueryUsercase(object):

    def __init__(self, db_session, user, ):
        self.db_session = db_session
        self.user = user
        self.light_collection = self.db_session['light']

    @except_logger("find_specified_light failed .....................")
    async def find_specified_light(self, light_id: str):
        try:
            filter = {'id': light_id}
            filter.update({"usr_id": self.user.id})
            result_dict = await self.light_collection.find_one(filter, {'_id': 0})
            if result_dict is None:
                raise LightNotFoundError
            return LightReadDTO(**result_dict)
        except:
            raise

    @except_logger("find_all_light failed .....................")
    async def find_all_light(self, p_num, p_size, content):
        try:
            filter = ({"usr_id": self.user.id})
            if content not in [""]:
                filter.update({"$or": [{"name": {"$regex": content, "$options": "i"}},
                                       {"desc": {"$regex": content, "$options": "i"}}]})
            total_num = await self.light_collection.count_documents(filter)
            total_page_num = math.ceil(total_num / p_size)
            if p_num > total_page_num and total_page_num > 0:
                p_num = total_page_num
            if p_num > 0:
                results_dict = self.light_collection.find(filter, {'_id': 0}).sort(
                    [('last_modified', -1)]).skip((p_num - 1) * p_size).limit(p_size).to_list(length=50)
            else:
                results_dict = self.light_collection.find(filter, {'_id': 0}).sort(
                    [('last_modified', -1)]).to_list(length=total_num)
            if results_dict:
                response_dic = {}
                response_dto_lst = []
                response_dic["total_num"] = total_num
                response_dic["total_page_num"] = total_page_num

                for doc in await results_dict:
                    response_dto_lst.append(LightReadDTO(**doc))
                response_dic["datas"] = response_dto_lst
                return response_dic
        except:
            raise
