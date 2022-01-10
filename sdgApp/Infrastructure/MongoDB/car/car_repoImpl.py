from datetime import datetime

from sdgApp.Domain.car.car import CarAggregate
from sdgApp.Domain.car.car_repo import CarRepo


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    ...


class CarRepoImpl(CarRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.car_collection = self.db_session['cars']

    def create(self, car: CarAggregate):
        car_DO = {"id": car.id,
                  "name": car.name,
                  "desc": car.desc,
                  "param": car.param}
        car_DO.update({"usr_id": self.user.id})
        car_DO.update({"create_time": datetime.now(),
                       "last_modified": None})

        self.car_collection.insert_one(car_DO)

    def delete(self, car_id: str):
        filter = {'id': car_id}
        filter.update({"usr_id": self.user.id})

        self.car_collection.delete_one(filter)

    def update(self, update_car: CarAggregate):
        update_car_DO = {"name": update_car.name,
                         "desc": update_car.desc,
                         "param": update_car.param}
        update_car_DO.update({"last_modified": datetime.now()})

        filter = {
            'id': update_car.id
        }
        filter.update({"usr_id": self.user.id})

        self.car_collection.update_one(filter
                                       , {'$set': update_car_DO})

    def get(self, car_id: str):
        filter = {'id': car_id}
        filter.update({"usr_id": self.user.id})

        result_DO = self.car_collection.find_one(filter, {'_id': 0, 'usr_id': 0})
        if result_DO:
            car = CarAggregate(id=result_DO["id"])
            car.save_DO_shortcut(result_DO)
            return car

    def list(self):
        filter = {"usr_id": self.user.id}
        car_aggregate_lst = []
        results_DO = self.car_collection.find(filter, {'_id': 0, 'usr_id': 0})
        if results_DO:
            for one_result in results_DO:
                one_car = CarAggregate(id=one_result["id"])
                one_car.save_DO_shortcut(one_result)
                car_aggregate_lst.append(one_car)
            return car_aggregate_lst
