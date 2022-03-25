from datetime import datetime
from sdgApp.Infrastructure.MongoDB.environment.env_DO import EnvDO
from sdgApp.Domain.environments.envs_repo import EnvsRepo
from sdgApp.Domain.environments.envs import EnvsAggregate
from fastapi import HTTPException


class EnvRepoImpl(EnvsRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.envs_collection = self.db_session['environments']

    def create_env(self, env: EnvsAggregate):
        env_DO = EnvDO(id=env.id,
                       name=env.name,
                       desc=env.desc,
                       weather_param=env.weather_param,
                       usr_id=self.user.id,
                       create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                       )
        self.envs_collection.insert_one(env_DO.dict())

    def delete_env(self, env_id: str):
        filter = {'id': env_id}
        self.envs_collection.delete_one(filter)

    def update_env(self, env_id: str, env: EnvsAggregate):
        update_env_DO = EnvDO(id=env.id,
                              name=env.name,
                              desc=env.desc,
                              weather_param=env.weather_param,
                              usr_id=None,
                              create_time=None,
                              last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                              )
        filter = {'id': env_id}
        self.envs_collection.update_one(filter, {'$set': update_env_DO.dict(exclude={'usr_id', 'create_time'})})

    def get(self, env_id: str):
        filter = {'id': env_id}
        result_dict = self.envs_collection.find_one(filter, {'_id': 0})
        if result_dict:
            dynamics = EnvDO(**result_dict).to_entity()
            return dynamics

    def list(self):
        filter = {}
        envs_lst = []
        results_dict = self.envs_collection.find(filter, {'_id': 0})
        if results_dict:
            for one_result in results_dict:
                one_env = EnvDO(**one_result).to_entity()
                envs_lst.append(one_env)
            return envs_lst

