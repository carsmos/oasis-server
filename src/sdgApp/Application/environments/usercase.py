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

    async def delete_env(self, env_id: str):
        try:
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

    async def find_all_envs(self, p_num):
        try:
            response_dto_lst = []
            filter = ({"usr_id": self.user.id})
            results_dict = self.envs_collection.find(filter, {'_id': 0}).sort([('last_modified', -1)])
            if results_dict:
                async for one_result in results_dict:
                    response_dto_lst.append(EnvReadDTO(**one_result))

                response_dto_lst = split_page(p_num, response_dto_lst)
                return response_dto_lst
        except:
            raise

