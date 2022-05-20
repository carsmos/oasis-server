import math

import shortuuid
import copy

from sdgApp.Application.car.CommandDTOs import CarCreateDTO, CarUpdateDTO
from sdgApp.Application.car.RespondsDTOs import CarReadDTO
from sdgApp.Domain.car.car import CarAggregate
from sdgApp.Domain.car.car_exceptions import CarNotFoundError
from sdgApp.Infrastructure.MongoDB.car.car_repoImpl import CarRepoImpl



class CarCommandUsercase(object):

    def __init__(self, db_session, user, repo=CarRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    async def create_car(self, car_create_model: CarCreateDTO):
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
            await self.repo.create(car)

        except:
            raise

    async def delete_car(self, car_id: str):
        try:
            await self.repo.delete(car_id)
        except:
            raise

    async def update_car(self, car_id:str, car_update_model: CarUpdateDTO):
        try:
            car_retrieved = await self.repo.get(car_id=car_id)

            car_retrieved.name = car_update_model.name
            car_retrieved.desc = car_update_model.desc
            car_retrieved.param = car_update_model.param
            car_retrieved.car_snap.update(car_update_model.car_snap)
            car_retrieved.sensors_snap.update(car_update_model.sensors_snap)
            car_retrieved.car_snap['car_name'] = car_update_model.name
            car_retrieved.sensors_snap['car_name'] = car_update_model.name

            await self.repo.update(car_retrieved)

        except:
            raise

    async def update_car_snap(self, car_id:str, dto: dict):
        try:
            car_snap_dict = dto
            snapshot_car = CarAggregate(car_id,
                                        name=car_snap_dict["name"],
                                        desc=car_snap_dict["desc"],
                                        param=car_snap_dict["param"],
                                        sensors_snap=car_snap_dict["sensors_snap"],
                                        car_snap=car_snap_dict["car_snap"])
            self.repo.update(snapshot_car)

            car = await self.repo.get(car_id=car_id)
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

    async def get_car(self, car_id:str):
        try:
            filter = {'id': car_id}
            if self.user:                     # used by carla ros backend
                filter.update({"usr_id": self.user.id})

            result_dict = await self.car_collection.find_one(filter, {'_id': 0, 'usr_id':0})
            if result_dict is None:
                raise CarNotFoundError
            return CarReadDTO(**result_dict)
        except:
            raise

    async def list_car(self, pagenum, pagesize, content):
        try:
            filter = {"usr_id": self.user.id}
            if content:
                filter.update({"$or": [{"name": {"$regex": content}}, {"desc":{"$regex": content}}]})
            total_num = await self.car_collection.count_documents(filter)
            total_page_num = math.ceil(total_num / pagesize)
            if pagenum > total_page_num > 0:
                pagenum = total_page_num
            if pagenum > 0:
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
                                                           'sensors_snap.sensors.sensor_id': 1,
                                                           'sensors_snap.sensors.type': 1}).sort([('last_modified', -1)]).skip((pagenum-1) * pagesize).limit(pagesize).to_list(length=50)
            else:
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
                                                                 'sensors_snap.sensors.sensor_id': 1,
                                                                 'sensors_snap.sensors.type': 1}).sort(
                    [('last_modified', -1)]).to_list(length=total_num)
            if results_dict:
                response_dic = {}
                response_dto_lst = []
                response_dic["total_num"] = total_num
                response_dic["total_page_num"] = total_page_num

                for doc in await results_dict:
                    sensors = doc.get('sensors_snap').get('sensors')
                    if sensors:
                        sensors_new = []
                        for sensor in sensors:
                            if sensor['sensor_id'] != 'default':
                                sensors_new.append(sensor)
                        doc['sensors_snap']['sensors'] = sensors_new
                    response_dto_lst.append(CarReadDTO(**doc))
                response_dic["datas"] = response_dto_lst
                return response_dic
        except:
            raise


def split_page(total_num, p_num, results_dict, res_model, limit: int = 15):
    total_page_num = math.ceil(total_num / limit)
    response_dic = {}
    response_dto_lst = []
    response_dic["total_num"] = total_num
    response_dic["total_page_num"] = total_page_num
    if p_num > total_page_num:
        p_num = total_page_num
    for one_result in results_dict.skip((p_num-1) * limit).limit(limit).to_list(length=50):
        response_dto_lst.append(res_model(**one_result))
    response_dic["datas"] = response_dto_lst
    return response_dic


