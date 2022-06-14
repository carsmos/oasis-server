import math

import shortuuid

from sdgApp.Application.car.usercase import split_page
from sdgApp.Application.dynamics.CommandDTOs import DynamicsCreateDTO, DynamicsUpdateDTO
from sdgApp.Application.dynamics.RespondsDTOs import DynamicsReadDTO
from sdgApp.Domain.dynamics.dynamics import DynamicsAggregate
from sdgApp.Domain.dynamics.dynamics_exceptions import DynamicsNotFoundError
from sdgApp.Infrastructure.MongoDB.dynamics.dynamics_repoImpl import DynamicsRepoImpl
from sdgApp.Application.log.usercase import except_logger

class DynamicsCommandUsercase(object):

    def __init__(self, db_session, user, repo=DynamicsRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)
    @except_logger("create_dynamics failed .....................")
    async def create_dynamics(self, dynamics_create_model: DynamicsCreateDTO):
        try:
            uuid = shortuuid.uuid()
            dynamics = DynamicsAggregate(id=uuid,
                                name=dynamics_create_model.name,
                                desc=dynamics_create_model.desc,
                                param=dynamics_create_model.param)
            await self.repo.create(dynamics)
        except:
            raise
    @except_logger("delete_dynamics failed .....................")
    async def delete_dynamics(self, dynamics_ids: str):
        try:
            for dynamics_id in dynamics_ids.split("+"):
                await self.repo.delete(dynamics_id)
        except:
            raise
    @except_logger("update_dynamics failed .....................")
    async def update_dynamics(self, dynamics_id:str, dynamics_update_model: DynamicsUpdateDTO):
        try:
            dynamics_retrieved = await self.repo.get(dynamics_id=dynamics_id)
            dynamics_retrieved.name = dynamics_update_model.name
            dynamics_retrieved.desc = dynamics_update_model.desc
            dynamics_retrieved.param = dynamics_update_model.param
            await self.repo.update(dynamics_retrieved)
        except:
            raise


class DynamicsQueryUsercase(object):

    def __init__(self, db_session, user, repo=DynamicsRepoImpl):
        self.db_session = db_session
        self.user = user
        self.dynamics_collection = self.db_session['dynamics']

    @except_logger("get_dynamics failed .....................")
    async def get_dynamics(self, dynamics_id:str):
        try:
            filter = {'id': dynamics_id}
            filter.update({"usr_id": self.user.id})

            result_dict = await self.dynamics_collection.find_one(filter, {'_id': 0, 'usr_id':0})
            if result_dict is None:
                raise DynamicsNotFoundError
            return DynamicsReadDTO(**result_dict)
        except:
            raise

    @except_logger("list_dynamics failed .....................")
    async def list_dynamics(self, p_num, p_size, content):
        try:
            filter = {"usr_id": self.user.id}
            if content not in [""]:
                filter.update({"$or": [{"name": {"$regex": content, "$options": "i"}},
                                       {"desc": {"$regex": content, "$options": "i"}}]})
            total_num = await self.dynamics_collection.count_documents(filter)
            total_page_num = math.ceil(total_num / p_size)
            if p_num > total_page_num and total_page_num > 0:
                p_num = total_page_num
            if p_num > 0:
                results_dict = self.dynamics_collection.find(filter, {'_id': 0, 'usr_id':0}).sort(
                    [('last_modified', -1)]).skip((p_num-1) * p_size).limit(p_size).to_list(length=50)
            else:
                results_dict = self.dynamics_collection.find(filter, {'_id': 0, 'usr_id': 0}).sort(
                    [('last_modified', -1)]).to_list(length=total_num)
            if results_dict:
                response_dic = {}
                response_dto_lst = []
                response_dic["total_num"] = total_num
                response_dic["total_page_num"] = total_page_num

                for doc in await results_dict:
                    response_dto_lst.append(DynamicsReadDTO(**doc))
                response_dic["datas"] = response_dto_lst
                return response_dic
        except:
            raise

