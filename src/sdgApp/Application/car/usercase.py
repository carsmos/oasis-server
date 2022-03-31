import shortuuid
import copy

from sdgApp.Application.car.CommandDTOs import CarCreateDTO, CarUpdateDTO
from sdgApp.Application.car.RespondsDTOs import CarReadDTO
from sdgApp.Domain.car.car import CarAggregate
from sdgApp.Infrastructure.MongoDB.car.car_repoImpl import CarRepoImpl



class CarCommandUsercase(object):

    def __init__(self, db_session, user, repo=CarRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def create_car(self, car_create_model: CarCreateDTO):
        try:
            uuid = shortuuid.uuid()

            car_create_model.sensors_snap['car_id'] = uuid
            car_create_model.sensors_snap['car_name'] = car_create_model.name
            car_create_model.car_snap['car_id'] = uuid
            car_create_model.car_snap['car_name'] = car_create_model.name

            car = CarAggregate(uuid,
                               name=car_create_model.name,
                               desc=car_create_model.desc,
                               param=car_create_model.param,
                               sensors_snap=car_create_model.sensors_snap,
                               car_snap=car_create_model.car_snap)
            self.repo.create(car)

        except:
            raise

    def delete_car(self, car_id: str):
        try:
            self.repo.delete(car_id)
        except:
            raise

    def update_car(self, car_id:str, car_update_model: CarUpdateDTO):
        try:
            car_retrieved = self.repo.get(car_id=car_id)

            car_retrieved.name = car_update_model.name
            car_retrieved.desc = car_update_model.desc
            car_retrieved.param = car_update_model.param
            car_retrieved.car_snap.update(car_update_model.car_snap)
            car_retrieved.sensors_snap.update(car_update_model.sensors_snap)
            car_retrieved.car_snap['car_name'] = car_update_model.name
            car_retrieved.sensors_snap['car_name'] = car_update_model.name

            self.repo.update(car_retrieved)

        except:
            raise

    def update_car_snap(self, car_id:str, dto: dict):
        try:
            car_snap_dict = dto
            snapshot_car = CarAggregate(car_id,
                                        name=car_snap_dict["name"],
                                        desc=car_snap_dict["desc"],
                                        param=car_snap_dict["param"],
                                        sensors_snap=car_snap_dict["sensors_snap"],
                                        car_snap=car_snap_dict["car_snap"])
            self.repo.update(snapshot_car)

            car = self.repo.get(car_id=car_id)
            if car:
                response_dto = dto_assembler(car)
                return response_dto

        except:
            raise




class CarQueryUsercase(object):

    def __init__(self, db_session, user, repo=CarRepoImpl):
        self.db_session = db_session
        self.user = user
        self.car_collection = self.db_session['cars']

    def get_car(self, car_id:str):
        try:
            filter = {'id': car_id}
            if self.user:                     # used by carla ros backend
                filter.update({"usr_id": self.user.id})

            result_dict = self.car_collection.find_one(filter, {'_id': 0, 'usr_id':0})
            return CarReadDTO(**result_dict)
        except:
            raise

    def list_car(self):
        try:
            response_dto_lst = []
            filter = {"usr_id": self.user.id}
            results_dict = self.car_collection.find(filter, {'name': 1,
                                                           'id': 1,
                                                           'desc': 1,
                                                           'param': 1,
                                                           'create_time': 1,
                                                           'last_modified': 1,
                                                           '_id': 0,
                                                           'car_snap.vehicle_physics_control.dynamics_name': 1,
                                                           'car_snap.vehicle_physics_control.dynamics_id': 1,
                                                           'car_snap.vehicle_physics_control.wheels.front_left_wheel.wheel_name': 1,
                                                           'car_snap.vehicle_physics_control.wheels.front_left_wheel.wheel_id': 1,
                                                           'car_snap.vehicle_physics_control.wheels.front_right_wheel.wheel_name': 1,
                                                           'car_snap.vehicle_physics_control.wheels.front_right_wheel.wheel_id': 1,
                                                           'car_snap.vehicle_physics_control.wheels.rear_left_wheel.wheel_name': 1,
                                                           'car_snap.vehicle_physics_control.wheels.rear_left_wheel.wheel_id': 1,
                                                           'car_snap.vehicle_physics_control.wheels.rear_right_wheel.wheel_name': 1,
                                                           'car_snap.vehicle_physics_control.wheels.rear_right_wheel.wheel_id': 1,
                                                           'sensors_snap.sensors.sensor_name': 1,
                                                           'sensors_snap.sensors.sensor_id': 1})
            if results_dict:
                for one_result in results_dict:
                    response_dto_lst.append(CarReadDTO(**one_result))
                return response_dto_lst

        except:
            raise

