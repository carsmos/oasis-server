from datetime import datetime

from sdgApp.Domain.dynamics.dynamics import DynamicsAggregate
from sdgApp.Domain.dynamics.dynamics_repo import DynamicsRepo


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    ...


class DynamicsRepoImpl(DynamicsRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.dynamics_collection = self.db_session['dynamics']

    def create(self, dynamics: DynamicsAggregate):
        dynamics_DO = {"id": dynamics.id,
                     "name": dynamics.name,
                     "car_id": dynamics.car_id,
                     "car_name": dynamics.car_name,
                     "desc": dynamics.desc,
                     "param": dynamics.param}
        dynamics_DO.update({"usr_id": self.user.id})
        dynamics_DO.update({"create_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       "last_modified": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

        self.dynamics_collection.insert_one(dynamics_DO)

    def delete(self, dynamics_id: str):
        filter = {'id': dynamics_id}
        filter.update({"usr_id": self.user.id})

        self.dynamics_collection.delete_one(filter)

    def update(self, update_dynamics: DynamicsAggregate):
        update_dynamics_DO = {"name": update_dynamics.name,
                            "car_id": update_dynamics.car_id,
                            "car_name": update_dynamics.car_name,
                            "desc": update_dynamics.desc,
                            "param": update_dynamics.param}
        update_dynamics_DO.update({"last_modified": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

        filter = {
            'id': update_dynamics.id
        }
        filter.update({"usr_id": self.user.id})
        self.dynamics_collection.update_one(filter
                                           , {'$set': update_dynamics_DO})

    def get(self, dynamics_id: str):
        filter = {'id': dynamics_id}
        filter.update({"usr_id": self.user.id})

        result_DO = self.dynamics_collection.find_one(filter, {'_id': 0, 'usr_id': 0})
        if result_DO:
            dynamics = DynamicsAggregate(id=result_DO["id"])
            dynamics.save_DO_shortcut(result_DO)
            return dynamics

    def list(self, query_param: dict):
        filter = {"usr_id": self.user.id}
        filter.update(query_param)

        dynamics_aggregate_lst = []
        results_DO = self.dynamics_collection.find(filter, {'_id': 0, 'usr_id': 0})
        if results_DO:
            for one_result in results_DO:
                one_dynamics = DynamicsAggregate(id=one_result["id"])
                one_dynamics.save_DO_shortcut(one_result)
                dynamics_aggregate_lst.append(one_dynamics)
            return dynamics_aggregate_lst
