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
                  "param": car.param,
                  "sensors_snap": car.sensors_snap,
                  "car_snap": car.car_snap}
        car_DO.update({"usr_id": self.user.id})
        car_DO.update({"create_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       "last_modified": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

        self.car_collection.insert_one(car_DO)

    def delete(self, car_id: str):
        filter = {'id': car_id}
        filter.update({"usr_id": self.user.id})

        self.car_collection.delete_one(filter)

    def update(self, update_car: CarAggregate):
        update_car_DO = {"name": update_car.name,
                         "desc": update_car.desc,
                         "param": update_car.param,
                         "sensors_snap": update_car.sensors_snap,
                         "car_snap": update_car.car_snap}
        update_car_DO.update({"last_modified": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

        filter = {
            'id': update_car.id
        }
        filter.update({"usr_id": self.user.id})

        self.car_collection.update_one(filter
                                       , {'$set': update_car_DO})

    def get(self, car_id: str):
        filter = {'id': car_id}
        if self.user:
            filter.update({"usr_id": self.user.id})

        result_DO = self.car_collection.find_one(filter, {'_id': 0, 'usr_id': 0})
        if result_DO:
            car = CarAggregate(id=result_DO["id"],
                               name=result_DO['name'],
                               desc=result_DO['desc'],
                               param=result_DO['param'],
                               sensors_snap=result_DO['sensors_snap'],
                               car_snap=result_DO['car_snap'])
            car.save_DO_shortcut(result_DO)
            return car

    def list(self):
        filter = {"usr_id": self.user.id}
        car_aggregate_lst = []
        results_DO = self.car_collection.find(filter, {'name':1,
                                                       'id':1,
                                                       'desc':1,
                                                       'param':1,
                                                       'create_time':1,
                                                       'last_modified':1,
                                                       '_id':0,
                                                       'car_snap.vehicle_physics_control.dynamics_name':1,
                                                       'car_snap.vehicle_physics_control.dynamics_id':1,
                                                       'car_snap.vehicle_physics_control.wheels.front_left_wheel.wheel_name':1,
                                                       'car_snap.vehicle_physics_control.wheels.front_left_wheel.wheel_id':1,
                                                       'car_snap.vehicle_physics_control.wheels.front_right_wheel.wheel_name':1,
                                                       'car_snap.vehicle_physics_control.wheels.front_right_wheel.wheel_id':1,
                                                       'car_snap.vehicle_physics_control.wheels.rear_left_wheel.wheel_name': 1,
                                                       'car_snap.vehicle_physics_control.wheels.rear_left_wheel.wheel_id': 1,
                                                       'car_snap.vehicle_physics_control.wheels.rear_right_wheel.wheel_name': 1,
                                                       'car_snap.vehicle_physics_control.wheels.rear_right_wheel.wheel_id': 1,
                                                       'sensors_snap.sensors.sensor_name':1,
                                                       'sensors_snap.sensors.sensor_id':1})
        if results_DO:
            for one_result in results_DO:
                one_car = CarAggregate(id=one_result["id"])
                one_car.save_DO_shortcut(one_result)
                car_aggregate_lst.append(one_car)
            return car_aggregate_lst
