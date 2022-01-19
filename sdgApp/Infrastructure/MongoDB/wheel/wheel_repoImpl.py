from datetime import datetime

from sdgApp.Domain.wheel.wheel import WheelAggregate
from sdgApp.Domain.wheel.wheel_repo import WheelRepo


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    ...


class WheelRepoImpl(WheelRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.wheel_collection = self.db_session['wheels']

    def create(self, wheel: WheelAggregate):
        wheel_DO = {"id": wheel.id,
                     "name": wheel.name,
                     "type": wheel.type,
                     "car_id": wheel.car_id,
                     "car_name": wheel.car_name,
                     "desc": wheel.desc,
                     "param": wheel.param}
        wheel_DO.update({"usr_id": self.user.id})
        wheel_DO.update({"create_time": datetime.now(),
                       "last_modified": datetime.now()})

        self.wheel_collection.insert_one(wheel_DO)

    def delete(self, wheel_id: str):
        filter = {'id': wheel_id}
        filter.update({"usr_id": self.user.id})

        self.wheel_collection.delete_one(filter)

    def update(self, update_wheel: WheelAggregate):
        update_wheel_DO = {"name": update_wheel.name,
                            "type": update_wheel.type,
                            "car_id": update_wheel.car_id,
                            "car_name": update_wheel.car_name,
                            "desc": update_wheel.desc,
                            "param": update_wheel.param}
        update_wheel_DO.update({"last_modified": datetime.now()})

        filter = {
            'id': update_wheel.id
        }
        filter.update({"usr_id": self.user.id})
        self.wheel_collection.update_one(filter
                                           , {'$set': update_wheel_DO})

    def get(self, wheel_id: str):
        filter = {'id': wheel_id}
        filter.update({"usr_id": self.user.id})

        result_DO = self.wheel_collection.find_one(filter, {'_id': 0, 'usr_id': 0})
        if result_DO:
            wheel = WheelAggregate(id=result_DO["id"])
            wheel.save_DO_shortcut(result_DO)
            return wheel

    def list(self, query_param: dict):
        filter = {"usr_id": self.user.id}
        filter.update(query_param)

        wheel_aggregate_lst = []
        results_DO = self.wheel_collection.find(filter, {'_id': 0, 'usr_id': 0})
        if results_DO:
            for one_result in results_DO:
                one_wheel = WheelAggregate(id=one_result["id"])
                one_wheel.save_DO_shortcut(one_result)
                wheel_aggregate_lst.append(one_wheel)
            return wheel_aggregate_lst
