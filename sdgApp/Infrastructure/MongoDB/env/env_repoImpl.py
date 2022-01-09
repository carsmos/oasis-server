from sdgApp.Domain.envs.envs_repo import EnvsRepo
from sdgApp.Domain.envs.envs import EnvsAggregate
from fastapi import HTTPException

def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    pass


class EnvRepoImpl(EnvsRepo):

    def __init__(self, db_session):
        self.db_session = db_session
        self.envs_collection = self.db_session['environments']

    def create(self, env: EnvsAggregate):
        env_DO = DataMapper_to_DO(env)
        result = self.envs_collection.insert_one(env_DO)
        return self.envs_collection.find_one({"_id": result.inserted_id})

    def delete(self, env_id: str):
        result = self.envs_collection.delete_one({"env_id": env_id})
        if result.deleted_count != 0:
            return {"status_code": 200, "Detail": "Delete data sucess"}

    def update(self, env_id: str, env):
        env_DO = DataMapper_to_DO(env)
        result = self.envs_collection.update_one(
            {
                'env_id': env_id,
            }, {'$set': env_DO})
        if result.matched_count == 1 and result.modified_count == 1:
            return True
        else:
            raise HTTPException(status_code=400, detail="update data failed")

    def find_all_envs(self):
        env_aggregate_list = []
        results_DO = self.envs_collection.find({}, {'_id': 0})
        for one_result in results_DO:
            one_env = EnvsAggregate()
            one_env.save_DO_shortcut(one_result)
            env_aggregate_list.append(one_env)
        return env_aggregate_list

    def find_specified_env(self, env_id: str):
        result_DO = self.envs_collection.find_one({"env_id": env_id}, {'_id': 0})
        if not result_DO:
            raise HTTPException(status_code=400, detail="data is not exist")
        env = EnvsAggregate()
        env.save_DO_shortcut(result_DO)
        return env

