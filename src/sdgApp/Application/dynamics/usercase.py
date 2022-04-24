import math

import shortuuid

from sdgApp.Application.car.usercase import split_page
from sdgApp.Application.dynamics.CommandDTOs import DynamicsCreateDTO, DynamicsUpdateDTO
from sdgApp.Application.dynamics.RespondsDTOs import DynamicsReadDTO
from sdgApp.Domain.dynamics.dynamics import DynamicsAggregate
from sdgApp.Domain.dynamics.dynamics_exceptions import DynamicsNotFoundError
from sdgApp.Infrastructure.MongoDB.dynamics.dynamics_repoImpl import DynamicsRepoImpl


class DynamicsCommandUsercase(object):

    def __init__(self, db_session, user, repo=DynamicsRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

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

    async def delete_dynamics(self, dynamics_id: str):
        try:
            await self.repo.delete(dynamics_id)
        except:
            raise

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

    async def list_dynamics(self, p_num, limit: int = 15):
        try:
            filter = {"usr_id": self.user.id}
            total_num = await self.dynamics_collection.count_documents({"usr_id": self.user.id})
            total_page_num = math.ceil(total_num / limit)
            if p_num > total_page_num:
                p_num = total_page_num
            results_dict = self.dynamics_collection.find(filter, {'_id': 0, 'usr_id':0}).sort([('last_modified', -1)]).skip((p_num-1) * limit).limit(limit).to_list(length=50)
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

