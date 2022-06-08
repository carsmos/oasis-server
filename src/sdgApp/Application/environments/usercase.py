import math

import shortuuid

from sdgApp.Application.car.usercase import split_page
from sdgApp.Application.environments.RespondsDTOs import EnvReadDTO
from sdgApp.Application.environments.CommandDTOs import EnvCreateDTO, EnvUpdateDTO
from sdgApp.Domain.environments.envs import EnvsAggregate
from sdgApp.Domain.environments.envs_exceptions import EnvNotFoundError
from sdgApp.Infrastructure.MongoDB.environment.env_repoImpl import EnvRepoImpl


class EnvCommandUsercase(object):

    def __init__(self, db_session, user, repo=EnvRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    async def create_env(self, env_create_model: EnvCreateDTO):
        try:
            uuid = shortuuid.uuid()
            env = EnvsAggregate(id=uuid,
                                name=env_create_model.name,
                                desc=env_create_model.desc,
                                weather_param=env_create_model.weather_param)
            await self.repo.create_env(env)
        except:
            raise

    async def delete_env(self, env_ids: str):
        try:
            for env_id in env_ids.split("+"):
                await self.repo.delete_env(env_id)
        except:
            raise

    async def update_env(self, env_id: str, env_create_model: EnvUpdateDTO):
        try:
            env_retrieved = await self.repo.get(env_id)
            env_retrieved.name = env_create_model.name
            env_retrieved.desc = env_create_model.desc
            env_retrieved.weather_param = env_create_model.weather_param
            await self.repo.update_env(env_id, env_retrieved)
        except:
            raise


class EnvQueryUsercase(object):

    def __init__(self, db_session, user,):
        self.db_session = db_session
        self.user = user
        self.envs_collection = self.db_session['environments']

    async def find_specified_env(self, env_id: str):
        try:
            filter = {'id': env_id}
            filter.update({"usr_id": self.user.id})
            result_dict = await self.envs_collection.find_one(filter, {'_id': 0})
            if result_dict is None:
                raise EnvNotFoundError
            return EnvReadDTO(**result_dict)
        except:
            raise

    async def find_all_envs(self, p_num, p_size, content):
        try:
            filter = ({"usr_id": self.user.id})
            if content not in [""]:
                filter.update({"$or": [{"name": {"$regex": content, "$options": "i"}},
                                       {"desc": {"$regex": content, "$options": "i"}}]})
            total_num = await self.envs_collection.count_documents(filter)
            total_page_num = math.ceil(total_num / p_size)
            if p_num > total_page_num and total_page_num > 0:
                p_num = total_page_num
            if p_num > 0:
                results_dict = self.envs_collection.find(filter, {'_id': 0}).sort(
                    [('last_modified', -1)]).skip((p_num-1) * p_size).limit(p_size).to_list(length=50)
            else:
                results_dict = self.envs_collection.find(filter, {'_id': 0}).sort(
                    [('last_modified', -1)]).to_list(length=total_num)
            if results_dict:
                response_dic = {}
                response_dto_lst = []
                response_dic["total_num"] = total_num
                response_dic["total_page_num"] = total_page_num

                for doc in await results_dict:
                    response_dto_lst.append(EnvReadDTO(**doc))
                response_dic["datas"] = response_dto_lst
                return response_dic
        except:
            raise

