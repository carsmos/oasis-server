import os
import utils.utils

from typing import List
from tortoise import transactions
from fastapi import APIRouter, status, Query, Body, Depends, Request
from apps.auth.auth_casbin import AuthorityRole
from apps.dynamic.model import Dynamics
from apps.job.model import Jobs

from apps.sensor.model import Sensors
from core.middleware import limiter
from core.settings import TIMES
from utils.auth import request
from tortoise.expressions import Q
from apps.car.schema import CarModel
from apps.car.model import Cars, CarSensors
from fastapi.encoders import jsonable_encoder

router = APIRouter()
sorted_list = ['sensor.lidar.goal', 'sensor.camera.goal', "sensor.camera.rgb", 'sensor.camera.depth',
               "sensor.camera.fisheye", 'sensor.lidar.ray_cast', 'sensor.lidar.ray_cast_mems',
               "sensor.other.radar", "sensor.other.ultrasonic", 'sensor.other.gnss', 'sensor.other.imu']


@router.post("/create_car",
             summary='创建车辆',
             tags=["Cars"])
@limiter.limit("%d/minute" %TIMES)
async def create_car(request: Request, car_model: CarModel):
    user = request.state.user
    assert not await Cars.filter(Q(company_id=user.company_id) | Q(system_data=1), name=car_model.name,
                                 invalid=0).first(), '车辆名称已存在，请更换'
    assert await Dynamics.filter(Q(company_id=user.company_id) | Q(system_data=1),
                                 id=car_model.dynamics_id, invalid=0).first(), '动力学模型不存在'
    car = Cars(**car_model.dict())
    car.user_id = user.id
    car.company_id = user.company_id
    car_info = car.__dict__
    await car.save()
    car_id = car.id
    sensors = []
    for sens in car_model.sensors:
        sensor = await Sensors.filter(Q(company_id=user.company_id) | Q(system_data=1), id=sens.sensor_id).first()
        assert sensor, '传感器模型不存在'
        sens = sens.dict()
        sens["car_id"] = car_id
        sens['company_id'] = user.company_id
        sens['name'] = sensor.name
        sens['name_en'] = sensor.name_en
        await CarSensors.create(**sens)
        if sens['type'] in ['sensor.camera.goal', 'sensor.lidar.goal']:
            car.render_mode = 'norender'
            await car.save()
        sensors.append(sens)
    car_info["sensors"] = sensors
    return car_info


@router.put("/update_car/{car_id}",
            summary='更新车辆',
            tags=["Cars"])
@limiter.limit("%d/minute" %TIMES)
async def update_car(request: Request, car_id, car_model: CarModel):
    user = request.state.user
    car_info = await Cars.filter(Q(company_id=user.company_id) | Q(system_data=1), id=car_id, invalid=0).first()
    assert car_info, '车辆不存在'
    assert not car_info.system_data, '系统内置车辆不可更改'
    if car_model.name != car_info.name:
        assert not await Cars.filter(Q(company_id=user.company_id) | Q(system_data=1), name=car_model.name,
                                     invalid=0).first(), '车辆名称已存在，请更换'
    await car_info.update_from_dict(car_model.dict()).save()
    sensors = []
    sensor_all_in_car = await CarSensors.filter(car_id=car_id, invalid=0).all()
    assert len(car_model.sensors) == len(set([(s.sensor_id, s.nick_name) for s in car_model.sensors])), '存在重名的传感器信息'
    if sensor_all_in_car:
        async with transactions.in_transaction():
            for s in sensor_all_in_car:
                if s.type in ['sensor.speedometer', 'sensor.opendrive_map']:
                    continue
                await CarSensors.filter(id=s.id).update(invalid=s.id)
    if car_model.sensors:
        for sens in car_model.sensors:
            sensor = await Sensors.filter(Q(company_id=user.company_id) | Q(system_data=1),
                                          id=sens.sensor_id).first()
            assert sensor, '传感器模型不存在'
            if sensor.type in ['sensor.camera.goal', 'sensor.lidar.goal'] and car_info.render_mode != 'norender':
                car_info.render_mode = 'norender'
                await car_info.save()
            sens = sens.dict()
            sens["car_id"] = car_id
            sens['name'] = sensor.name
            sens['name_en'] = sensor.name_en
            await CarSensors.create(**sens)
            sensors.append(sens)
    return


@router.delete(
    "/delete_car",
    summary='批量删除车辆',
    tags=["Cars"],
    dependencies=[Depends(AuthorityRole('admin'))])
@limiter.limit("%d/minute" %TIMES)
async def delete_car(request: Request, car_ids: List[int] = Body(..., embed=True)):
    user = request.state.user
    async with transactions.in_transaction():
        cars = await Cars.filter(Q(company_id=user.company_id) | Q(system_data=1), id__in=car_ids, invalid=0).all()
        assert cars, '车辆不存在'
        for car in cars:
            assert not car.system_data, '系统内置车辆不可删除'
            car.invalid = car.id
        await Cars.bulk_update(cars, fields=['invalid'])

        sensors = await CarSensors.filter(id__in=car_ids, invalid=0, system_data=0).all()
        if sensors:
            for sen in sensors:
                sen.invalid = sen.car_id
            await CarSensors.bulk_update(sensors, fields=['invalid'])
    return 'ok'


@router.delete(
    "/delete_car/{car_id}",
    summary='删除特定车辆',
    tags=["Cars"],
    dependencies=[Depends(AuthorityRole('admin'))])
@limiter.limit("5/minute")
async def delete_car(request: Request, car_id: int, real_exec: int = Body(0, embed=True), jobs: dict = Body({}, embed=True)):
    user = request.state.user
    async with transactions.in_transaction():
        car = await Cars.filter(Q(company_id=user.company_id) | Q(system_data=1), id=car_id, invalid=0).first()
        assert car, '车辆不存在'
        assert not car.system_data, '系统内置车辆不可删除'
        job_list = await Jobs.filter(company_id=user.company_id, invalid=0, status='waiting', car_id=car_id).all()
        if real_exec == 0:
            return job_list
        else:
            assert len(jobs) == len(job_list), '存在未处理的作业信息'
            for j in job_list:
                job = jobs.get(str(j.id), {})
                if job['action'] == 'replace':
                    j.car_id = job['car_id']
                    await j.save()

        sensors = await CarSensors.filter(car_id=car_id, invalid=0, system_data=0).all()
        if sensors:
            for sen in sensors:
                sen.invalid = sen.car_id
            await CarSensors.bulk_update(sensors, fields=['invalid'])
        car.invalid = car.id
        await car.save()
    return 'ok'


@router.get("/get_car",
            summary='获取特定车辆',
            tags=["Cars"])
async def get_car(car_id: int, overview=None):
    user = request.state.user
    car = await Cars.filter(Q(company_id=user.company_id) | Q(system_data=1), id=car_id, invalid=0).first()
    assert car, "车辆不存在"
    car_sensors = await CarSensors.filter(car_id=car_id, invalid=0).all().values()
    sensors = {"radar": [], "lidar": [], "imu": [], "gnss": [], "camera": [], "goal": [], "ultrasonic": []}
    if car_sensors:
        for sensor in car_sensors:
            if sensor["type"] == "sensor.other.imu":
                sensors["imu"].append(sensor)
            # elif sensor["type"] == "sensor.speedometer":
            #     sensors["speedometer"].append(sensor)
            # elif sensor["type"] == "sensor.opendrive_map":
            #     sensors["opendrive_map"].append(sensor)
            elif sensor["type"] == "sensor.other.ultrasonic":
                sor = await Sensors.filter(id=sensor['sensor_id'], invalid=0).first()
                assert sor, "传感器不存在"
                sensor['range'] = sor.param.get('range', '')
                sensor['horizontal_fov'] = sor.param.get('horizontal_fov', '')
                sensor['vertical_fov'] = sor.param.get('vertical_fov', '')
                sensors["ultrasonic"].append(sensor)
            elif sensor["type"] in ["sensor.lidar.ray_cast", "sensor.lidar.ray_cast_mems"]:
                sor = await Sensors.filter(id=sensor['sensor_id'], invalid=0).first()
                assert sor, "传感器不存在"
                sensor['range'] = sor.param.get('range', '')
                sensor['upper_fov'] = sor.param.get('upper_fov', '')
                sensor['lower_fov'] = sor.param.get('low_fov', '')
                sensors["lidar"].append(sensor)
            elif sensor["type"] == "sensor.other.gnss":
                sensors["gnss"].append(sensor)
            elif sensor["type"] == "sensor.other.radar":
                sor = await Sensors.filter(id=sensor['sensor_id'], invalid=0).first()
                assert sor, "传感器不存在"
                sensor['range'] = sor.param.get('range', '')
                sensor['horizontal_fov'] = sor.param.get('horizontal_fov', '')
                sensor['vertical_fov'] = sor.param.get('vertical_fov', '')
                sensors["radar"].append(sensor)
            elif sensor["type"] in ["sensor.camera.depth", "sensor.camera.rgb", "sensor.camera.fisheye"]:
                sor = await Sensors.filter(id=sensor['sensor_id'], invalid=0).first()
                assert sor, "传感器不存在"
                sensor['focal_distance'] = sor.param.get('focal_distance', '')
                sensor['fov'] = sor.param.get('fov', '')
                sensor['image_size_x'] = sor.param.get('image_size_x', '')
                sensor['image_size_y'] = sor.param.get('image_size_y', '')
                sensors["camera"].append(sensor)
            elif sensor["type"] in ['sensor.camera.goal', 'sensor.lidar.goal']:
                sor = await Sensors.filter(id=sensor['sensor_id'], invalid=0).first()
                assert sor, "传感器不存在"
                sensor['range'] = sor.param.get('range', '')
                sensor['horizontal_fov'] = sor.param.get('horizontal_fov', '')
                sensor['upper_fov'] = sor.param.get('upper_fov', '')
                sensor['lower_fov'] = sor.param.get('low_fov', '')
                sensor['image_size_x'] = sor.param.get('image_size_x', '')
                sensor['image_size_y'] = sor.param.get('image_size_y', '')
                sensors["goal"].append(sensor)
    if not overview:
        return {"car": car, "sensors": sensors}
    else:
        sensor_list = []
        for sens in car_sensors:
            if sens['type'] not in ["sensor.speedometer", "sensor.opendrive_map"]:
                sensor = await Sensors.filter(Q(company_id=user.company_id) | Q(system_data=1), invalid=0,
                                              id=sens["sensor_id"]).first()
                sensor_dict = jsonable_encoder(sensor)
                sensor_dict['position'] = {"x": sens.get('position_x'), "y": sens.get('position_y'),
                                           'z': sens.get('position_z'), 'roll': sens.get('roll'),
                                           'pitch': sens.get('pitch'), 'yaw': sens.get('yaw')}
                sensor_list.append(sensor_dict)
        dynamic = await Dynamics.filter(Q(company_id=user.company_id) | Q(system_data=1), invalid=0,
                                        id=car.dynamics_id).first()
        return {"car": car, "sensor_list": sensor_list, "dynamic": dynamic}


@router.get(
    "/cars",
    summary='获取所有车辆',
    tags=["Cars"]
)
async def get_all_cars(pagenum: int = 1, pagesize: int = 10, content: str = ""):
    user = request.state.user
    cars_model = Cars.filter(Q(company_id=user.company_id) | Q(system_data=1), invalid=0).all()
    if content:
        cars_model = cars_model.filter(Q(name__contains=content) | Q(desc__contains=content), invalid=0)

    total_num = await cars_model.count()
    if pagesize == 0:
        res = await cars_model.all()
    else:
        res = await cars_model.limit(pagesize).offset(max(0, pagenum - 1) * pagesize).all()
    pageinfo = utils.utils.paginate(total_num, pagesize)

    data = []
    for model in res:
        car_id = model.id
        car_sensors = await CarSensors.filter(car_id=car_id, invalid=0).all()
        model = jsonable_encoder(model)
        model['sensor_list'] = jsonable_encoder(car_sensors)
        model['sensors'] = []
        for type in sorted_list:
            for sens in model['sensor_list']:
                if type == sens.get("type"):
                    model['sensors'].append(sens)
        data.append(model)
    data = sorted(data, key=lambda v: v['modified_at'], reverse=True)
    return {'pageinfo': pageinfo, 'datas': data}
