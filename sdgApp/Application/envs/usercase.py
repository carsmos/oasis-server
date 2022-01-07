from sdgApp.Application.envs.RespondsDTOs import EnvReadDTO
from sdgApp.Application.envs.CommandDTOs import EnvCreateDTO, EnvUpdateDTO
from sdgApp.Domain.envs.envs import EnvsAggregate
from sdgApp.Infrastructure.MongoDB.env.env_repoImpl import EnvRepoImpl
from sdgApp.Infrastructure.MongoDB.session_maker import mongo_session


class EnvCommandUsercase(object):

    def __init__(self, repo=EnvRepoImpl, db_session=mongo_session):
        self.repo = repo
        _, db = db_session()
        self.repo = self.repo(db)

    def create_env(self, dto: EnvCreateDTO):
        try:
            env_dict = dto.dict()
            env = EnvsAggregate(env_id=env_dict["env_id"],
                                env_name=env_dict["env_name"],
                                desc=env_dict["desc"],
                                create_time=env_dict["create_time"],
                                wetness=env_dict["wetness"],
                                cloudiness=env_dict["cloudiness"],
                                fog_density=env_dict["fog_density"],
                                fog_falloff=env_dict["fog_falloff"],
                                fog_distance=env_dict["fog_distance"],
                                precipitation=env_dict["precipitation"],
                                wind_intensity=env_dict["wind_intensity"],
                                sun_azimuth_angle=env_dict["sun_azimuth_angle"],
                                sun_altitude_angle=env_dict["sun_altitude_angle"],
                                precipitation_deposits=env_dict["precipitation_deposits"])
            env.save_DO_shortcut(env_dict)
            return self.repo.create(env)
        except:
            raise


class EnvDeleteUsercase(object):

    def __init__(self, repo=EnvRepoImpl, db_session=mongo_session):
        self.repo = repo
        _, db = db_session()
        self.repo = self.repo(db)

    def delete_env(self, env_id: str):
        try:
            return self.repo.delete(env_id)
        except:
            raise


class EnvUpdateUsercase(object):

    def __init__(self, repo=EnvRepoImpl, db_session=mongo_session):
        self.repo = repo
        _, db = db_session()
        self.repo = self.repo(db)

    def update_env(self, env_id: str, dto: EnvUpdateDTO):
        try:
            env_dict = dto.dict()
            env = EnvsAggregate(env_id=env_dict["env_id"],
                                env_name=env_dict["env_name"],
                                desc=env_dict["desc"],
                                create_time=env_dict["create_time"],
                                wetness=env_dict["wetness"],
                                cloudiness=env_dict["cloudiness"],
                                fog_density=env_dict["fog_density"],
                                fog_falloff=env_dict["fog_falloff"],
                                fog_distance=env_dict["fog_distance"],
                                precipitation=env_dict["precipitation"],
                                wind_intensity=env_dict["wind_intensity"],
                                sun_azimuth_angle=env_dict["sun_azimuth_angle"],
                                sun_altitude_angle=env_dict["sun_altitude_angle"],
                                precipitation_deposits=env_dict["precipitation_deposits"])
            env.save_DO_shortcut(env_dict)
            return self.repo.update(env_id, env)
        except:
            raise


class EnvQueryUsercase(object):

    def __init__(self, repo=EnvRepoImpl, db_session=mongo_session):
        self.repo = repo
        _, db = db_session()
        self.repo = self.repo(db)

    def find_all_envs(self):
        try:
            return self.repo.find_all_envs()
        except:
            raise

    def find_specified_env(self, env_id: str):
        try:
            return self.repo.find_specified_env(env_id)
        except:
            raise
