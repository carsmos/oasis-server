import shortuuid

from sdgApp.Application.environments.CommandDTOs import EnvCreateDTO, EnvUpdateDTO
from sdgApp.Domain.environments.envs import EnvsAggregate
from sdgApp.Infrastructure.MongoDB.environment.env_repoImpl import EnvRepoImpl


def dto_assembler(env: EnvsAggregate):
    return env.shortcut_DO


class EnvCommandUsercase(object):

    def __init__(self, db_session, user, repo=EnvRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def create_env(self, dto: dict):
        try:
            uuid = shortuuid.uuid()
            env_dict = dto
            env = EnvsAggregate(uuid,
                                name=env_dict["name"],
                                desc=env_dict["desc"],
                                weather_param=env_dict["weather_param"])
            return self.repo.create_env(env)
        except:
            raise

    def delete_env(self, env_id: str):
        try:
            return self.repo.delete_env(env_id)
        except:
            raise

    def update_env(self, env_id: str, dto: dict):
        try:
            env_dict = dto
            env = EnvsAggregate(env_id,
                                name=env_dict["name"],
                                desc=env_dict["desc"],
                                weather_param=env_dict["weather_param"])
            return self.repo.update_env(env_id, env)
        except:
            raise


class EnvQueryUsercase(object):

    def __init__(self, db_session, user, repo=EnvRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def find_all_envs(self):
        try:
            response_dto_list = []
            env_list = self.repo.find_all_envs()
            for env in env_list:
                response_dto = dto_assembler(env)
                response_dto_list.append(response_dto)
            return response_dto_list
        except:
            raise

    def find_specified_env(self, env_id: str):
        try:
            env = self.repo.find_specified_env(env_id)
            response_dto = dto_assembler(env)
            return response_dto
        except:
            raise