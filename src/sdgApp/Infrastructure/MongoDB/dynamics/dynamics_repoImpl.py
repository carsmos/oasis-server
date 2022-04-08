from datetime import datetime

from sdgApp.Domain.dynamics.dynamics import DynamicsAggregate
from sdgApp.Domain.dynamics.dynamics_repo import DynamicsRepo
from sdgApp.Infrastructure.MongoDB.dynamics.dynamics_DO import DynamicsDO


class DynamicsRepoImpl(DynamicsRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.dynamics_collection = self.db_session['dynamics']

    async def create(self, dynamics: DynamicsAggregate):
        
        dynamics_DO = DynamicsDO(id=dynamics.id,
                                 name=dynamics.name,
                                 desc=dynamics.desc,
                                 param=dynamics.param,
                                 usr_id=self.user.id,
                                 create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                 last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        await self.dynamics_collection.insert_one(dynamics_DO.dict())

    async def delete(self, dynamics_id: str):
        filter = {'id': dynamics_id}
        filter.update({"usr_id": self.user.id})

        await self.dynamics_collection.delete_one(filter)

    async def update(self, update_dynamics: DynamicsAggregate):
        update_dynamics_DO = DynamicsDO(id=update_dynamics.id,
                                 name=update_dynamics.name,
                                 desc=update_dynamics.desc,
                                 param=update_dynamics.param,
                                 usr_id=None,
                                 create_time=None,
                                 last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        filter = {
            'id': update_dynamics.id
        }
        filter.update({"usr_id": self.user.id})
        await self.dynamics_collection.update_one(filter
                                           , {'$set': update_dynamics_DO.dict(exclude={'usr_id', 'create_time'})})

    async def get(self, dynamics_id: str):
        filter = {'id': dynamics_id}
        filter.update({"usr_id": self.user.id})

        result_dict = await self.dynamics_collection.find_one(filter, {'_id': 0})
        if result_dict:
            dynamics = DynamicsDO(**result_dict).to_entity()
            return dynamics

    async def list(self):
        filter = {"usr_id": self.user.id}
        dynamics_aggregate_lst = []
        results_dict = self.dynamics_collection.find(filter, {'_id': 0})
        if results_dict:
            async for one_result in results_dict:
                one_dynamics = DynamicsDO(**one_result).to_entity()
                dynamics_aggregate_lst.append(one_dynamics)
            return dynamics_aggregate_lst
