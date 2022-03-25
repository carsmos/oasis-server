import shortuuid
from sdgApp.Application.environments.RespondsDTOs import EnvReadDTO
from sdgApp.Application.environments.CommandDTOs import EnvCreateDTO, EnvUpdateDTO
from sdgApp.Domain.environments.envs import EnvsAggregate
from sdgApp.Infrastructure.MongoDB.environment.env_repoImpl import EnvRepoImpl


class EnvCommandUsercase(object):

    def __init__(self, db_session, user, repo=EnvRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def create_env(self, env_create_model: EnvCreateDTO):
        try:
            uuid = shortuuid.uuid()
            env = EnvsAggregate(id=uuid,
                                name=env_create_model.name,
                                desc=env_create_model.desc,
                                weather_param=env_create_model.weather_param)
            self.repo.create_env(env)
        except:
            raise

    def delete_env(self, env_id: str):
        try:
            self.repo.delete_env(env_id)
        except:
            raise

    def update_env(self, env_id: str, env_create_model: EnvUpdateDTO):
        try:
            env_retrieved = self.repo.get(env_id)
            env_retrieved.name = env_create_model.name
            env_retrieved.desc = env_create_model.desc
            env_retrieved.weather_param = env_create_model.weather_param
            self.repo.update_env(env_id, env_retrieved)
        except:
            raise


class EnvQueryUsercase(object):

    def __init__(self, db_session, user,):
        self.db_session = db_session
        self.user = user
        self.envs_collection = self.db_session['environments']

    def find_specified_env(self, env_id: str):
        try:
            filter = {'id': env_id}
            result_dict = self.envs_collection.find_one(filter, {'_id': 0})
            return EnvReadDTO(**result_dict)
        except:
            raise

    def find_all_envs(self):
        try:
            response_dto_lst = []
            filter = {}
            results_dict = self.envs_collection.find(filter, {'_id': 0})
            if results_dict:
                for one_result in results_dict:
                    response_dto_lst.append(EnvReadDTO(**one_result))
                return response_dto_lst
        except:
            raise

