from sdgApp.Domain.wheel.wheel import WheelAggregate
from sdgApp.Domain.wheel.wheel_repo import WheelRepo


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    ...


class WheelRepoImpl(WheelRepo):

    def __init__(self, db_session):
        self.db_session = db_session
        self.wheel_collection = self.db_session['wheels']

    def create(self, wheel: WheelAggregate):
        wheel_DO = {"id": wheel.id,
                     "name": wheel.name,
                     "car_id": wheel.car_id,
                     "car_name": wheel.car_name,
                     "desc": wheel.desc,
                     "param": wheel.param}

        self.wheel_collection.insert_one(wheel_DO)

    def delete(self, wheel_id: str):
        filter = {'id': wheel_id}
        self.wheel_collection.delete_one(filter)

    def update(self, update_wheel: WheelAggregate):
        update_wheel_DO = {"name": update_wheel.name,
                            "car_id": update_wheel.car_id,
                            "car_name": update_wheel.car_name,
                            "desc": update_wheel.desc,
                            "param": update_wheel.param}

        filter = {
            'id': update_wheel.id
        }
        self.wheel_collection.update_one(filter
                                           , {'$set': update_wheel_DO})

    def get(self, wheel_id: str):
        filter = {'id': wheel_id}
        result_DO = self.wheel_collection.find_one(filter, {'_id': 0})
        wheel = WheelAggregate(id=result_DO["id"])
        wheel.save_DO_shortcut(result_DO)
        return wheel

    def list(self):
        wheel_aggregate_lst = []
        results_DO = self.wheel_collection.find({}, {'_id': 0})
        for one_result in results_DO:
            one_wheel = WheelAggregate(id=one_result["id"])
            one_wheel.save_DO_shortcut(one_result)
            wheel_aggregate_lst.append(one_wheel)
        return wheel_aggregate_lst
