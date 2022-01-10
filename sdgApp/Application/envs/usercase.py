import shortuuid

from sdgApp.Application.envs.CommandDTOs import EnvCreateDTO, EnvUpdateDTO
from sdgApp.Domain.envs.envs import EnvsAggregate
from sdgApp.Infrastructure.MongoDB.env.env_repoImpl import EnvRepoImpl


def DTO_assembler(env: EnvsAggregate):
    return env.shortcut_DO


class EnvCommandUsercase(object):

    def __init__(self, db_session, repo=EnvRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session)

    def create_env(self, dto: EnvCreateDTO):
        try:
            uuid = shortuuid.uuid()
            env_dict = dto.dict()
            env = EnvsAggregate(uuid,
                                name=env_dict["name"],
                                desc=env_dict["desc"],
                                param=env_dict["param"])
            return self.repo.create_env(env)
        except:
            raise

    def delete_env(self, env_id: str):
        try:
            return self.repo.delete_env(env_id)
        except:
            raise

    def update_env(self, env_id: str, dto: EnvUpdateDTO):
        try:
            env_dict = dto.dict()
            env = EnvsAggregate(env_id,
                                name=env_dict["name"],
                                desc=env_dict["desc"],
                                param=env_dict["param"])
            return self.repo.update_env(env_id, env)
        except:
            raise


class EnvQueryUsercase(object):

    def __init__(self, db_session, repo=EnvRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session)

    def find_all_envs(self):
        try:
            response_dto_list = []
            env_list = self.repo.find_all_envs()
            for env in env_list:
                response_dto = DTO_assembler(env)
                response_dto_list.append(response_dto)
            return response_dto_list
        except:
            raise

    def find_specified_env(self, env_id: str):
        try:
            env = self.repo.find_specified_env(env_id)
            response_dto = DTO_assembler(env)
            return response_dto
        except:
            raise
