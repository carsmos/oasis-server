from sdgApp.Application.envs.RespondsDTOs import EnvReadDTO
from sdgApp.Application.envs.CommandDTOs import EnvCreateDTO, EnvUpdateDTO
from sdgApp.Domain.envs.envs import EnvsAggregate
from sdgApp.Infrastructure.MongoDB.env.env_repoImpl import EnvRepoImpl
from sdgApp.Infrastructure.MongoDB.session_maker import mongo_session


def DTO_assembler(env: EnvsAggregate):
    return env.shortcut_DO


class EnvCommandUsercase(object):

    def __init__(self, db_session, repo=EnvRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session)

    def create_env(self, dto: EnvCreateDTO):
        try:
            env_dict = dto.dict()
            env = EnvsAggregate(env_id=env_dict["env_id"],
                                env_name=env_dict["env_name"],
                                desc=env_dict["desc"],
                                create_time=env_dict["create_time"],
                                param=env_dict["param"])
            env.save_DO_shortcut(env_dict)
            return self.repo.create(env)
        except:
            raise


class EnvDeleteUsercase(object):

    def __init__(self, db_session, repo=EnvRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session)

    def delete_env(self, env_id: str):
        try:
            return self.repo.delete(env_id)
        except:
            raise


class EnvUpdateUsercase(object):

    def __init__(self, db_session, repo=EnvRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session)

    def update_env(self, env_id: str, dto: EnvUpdateDTO):
        try:
            env_dict = dto.dict()
            env = EnvsAggregate(env_id=env_dict["env_id"],
                                env_name=env_dict["env_name"],
                                desc=env_dict["desc"],
                                create_time=env_dict["create_time"],
                                param=env_dict["param"])
            env.save_DO_shortcut(env_dict)
            return self.repo.update(env_id, env)
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
