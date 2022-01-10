from sdgApp.Domain.dynamics.dynamics import DynamicsAggregate
from sdgApp.Domain.dynamics.dynamics_repo import DynamicsRepo


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    ...


class DynamicsRepoImpl(DynamicsRepo):

    def __init__(self, db_session):
        self.db_session = db_session
        self.dynamics_collection = self.db_session['dynamics']

    def create(self, dynamics: DynamicsAggregate):
        dynamics_DO = {"id": dynamics.id,
                     "name": dynamics.name,
                     "car_id": dynamics.car_id,
                     "car_name": dynamics.car_name,
                     "desc": dynamics.desc,
                     "param": dynamics.param}

        self.dynamics_collection.insert_one(dynamics_DO)

    def delete(self, dynamics_id: str):
        filter = {'id': dynamics_id}
        self.dynamics_collection.delete_one(filter)

    def update(self, update_dynamics: DynamicsAggregate):
        update_dynamics_DO = {"name": update_dynamics.name,
                            "car_id": update_dynamics.car_id,
                            "car_name": update_dynamics.car_name,
                            "desc": update_dynamics.desc,
                            "param": update_dynamics.param}

        filter = {
            'id': update_dynamics.id
        }
        self.dynamics_collection.update_one(filter
                                           , {'$set': update_dynamics_DO})

    def get(self, dynamics_id: str):
        filter = {'id': dynamics_id}
        result_DO = self.dynamics_collection.find_one(filter, {'_id': 0})
        dynamics = DynamicsAggregate(id=result_DO["id"])
        dynamics.save_DO_shortcut(result_DO)
        return dynamics

    def list(self):
        dynamics_aggregate_lst = []
        results_DO = self.dynamics_collection.find({}, {'_id': 0})
        for one_result in results_DO:
            one_dynamics = DynamicsAggregate(id=one_result["id"])
            one_dynamics.save_DO_shortcut(one_result)
            dynamics_aggregate_lst.append(one_dynamics)
        return dynamics_aggregate_lst
