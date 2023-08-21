import datetime
import random
import time

from tortoise.transactions import in_transaction

import utils.utils

from pydantic.typing import List, Optional
from core.settings import TIMES
from apps.auth.auth_casbin import AuthorityRole
from apps.car.model import CarSensors
from apps.sensor.schema import SensorModel
from apps.sensor.model import Sensors
from fastapi import APIRouter, status, Body, Depends, Request
from tortoise.expressions import Q

from core.middleware import limiter
from utils.auth import request

router = APIRouter()

cam_type_list = ['sensor.camera.depth', 'sensor.camera.rgb', "sensor.camera.fisheye"]
radar_type_list = ['sensor.other.radar', 'sensor.radar.goal']
goal_type_list = ['sensor.camera.goal', 'sensor.lidar.goal']
lidar_type_list = ['sensor.lidar.ray_cast', 'sensor.lidar.ray_cast_mems']


@router.post(
    "/sensors",
    summary='创建传感器',
    tags=["Sensors"]
)
@limiter.limit("%d/minute" %TIMES)
async def create_sensor(request: Request, sensor: SensorModel):
    user = request.state.user
    assert not await Sensors.filter(Q(company_id=user.company_id) | Q(system_data=1),
                                    name=sensor.name, invalid=0).first(), '传感器名称已存在'
    sensor = Sensors(**sensor.dict())
    fps = sensor.param.get("FPS", 1)
    sensor.param['sensor_tick'] = round(1 / fps, 2)
    if sensor.type in cam_type_list:
        sensor.group_type = 'cam'
    elif sensor.type in radar_type_list:
        sensor.group_type = 'radar'
    elif sensor.type in lidar_type_list:
        sensor.group_type = 'lidar'
    elif sensor.type == "sensor.other.ultrasonic":
        sensor.group_type = "ultrasonic"
    elif "imu" in sensor.type:
        sensor.group_type = 'imu'
    elif "gnss" in sensor.type:
        sensor.group_type = "gnss"
    # elif "speedometer" in sensor.type:
    #     sensor.group_type = "speedometer"
    # elif "opendrive_map" in sensor.type:
    #     sensor.group_type = "opendrive_map"
    elif sensor.type in goal_type_list:
        sensor.group_type = "goal"
    sensor.user_id = user.id
    sensor.company_id = user.company_id
    await sensor.save()
    return sensor


@router.delete(
    "/sensors/{sensor_id}",
    summary='删除传感器',
    tags=["Sensors"],
    dependencies=[Depends(AuthorityRole('admin'))]
)
@limiter.limit("%d/minute" %TIMES)
async def delete_sensor(request: Request, sensor_id: int, real_exec: int = Body(0, embed=True),
                        carsensors: dict = Body({}, embed=True)):
    user = request.state.user
    sensor_info = await Sensors.filter(Q(company_id=user.company_id) | Q(system_data=1), id=sensor_id,
                                       invalid=0).first()
    assert sensor_info, '传感器不存在'
    assert not sensor_info.system_data, '系统内置传感器不能删除'
    car_list = []
    async with in_transaction() as trans:
        cs = await trans.execute_query(
            'select carsensors.*,cars.name as car_name from carsensors left join cars on carsensors.car_id = cars.id where sensor_id = %s and carsensors.invalid = 0',
            (sensor_id,))
        car_list = cs[1]
    if not real_exec:
        return car_list
    else:
        assert len(car_list) == len(carsensors), '存在未处理的车辆信息'
        for c in car_list:
            carsensor = carsensors.get(str(c['id']), {})
            print('carsensor:', carsensor)
            if carsensor['action'] == 'delete':
                await CarSensors.filter(id=c['id']).update(invalid=c['id'])
            if carsensor['action'] == 'replace':
                replace_sensor = await Sensors.filter(id=carsensor['sensor_id']).first()
                await CarSensors.filter(id=c['id']).update(sensor_id=replace_sensor.id,
                                                           name=replace_sensor.name,
                                                           nick_name=replace_sensor.name + str(
                                                               int(time.time() + random.randint(1, 10))),
                                                           type=replace_sensor.type)

    sensor_info.invalid = sensor_id
    res = await sensor_info.save()
    # sensors = await CarSensors.filter(id=sensor_id, invalid=0, system_data=0).first()
    # await sensors,''
    # if sensors:
    #     for sen in sensors:
    #         sen.invalid = sen.car_id
    #     await CarSensors.bulk_update(sensors, fields=['invalid'])
    return res


@router.put(
    "/sensors/{sensor_id}",
    summary='更新传感器',
    tags=["Sensors"]
)
@limiter.limit("%d/minute" %TIMES)
async def update_sensor(request: Request, sensor_id: int, sensor_update: SensorModel):
    user = request.state.user
    sensor_info = await Sensors.filter(Q(company_id=user.company_id) | Q(system_data=1), id=sensor_id,
                                       invalid=0).first()
    assert sensor_info, '传感器不存在'
    assert not sensor_info.system_data, '系统内置传感器不能修改'
    if sensor_info.name != sensor_update.name:
        assert not await Sensors.filter(Q(company_id=user.company_id) | Q(system_data=1), name=sensor_update.name,
                                        invalid=0).first(), '传感器名称已存在，请更换'
    sensor_dict = sensor_update.dict()
    # 计算帧率
    fps = sensor_dict.get("param").get("FPS", 1)
    sensor_dict["param"]['sensor_tick'] = round(1 / fps, 2)
    res = await sensor_info.update_from_dict(sensor_dict).save()
    carsensor = await CarSensors.filter(sensor_id=sensor_id, invalid=0).first()
    if carsensor:
        carsensor.name = sensor_update.name
        await carsensor.save()
    return res


@router.get(
    "/sensors/{sensor_id}",
    summary='获取传感器',
    tags=["Sensors"]
)
async def get_sensor(sensor_id: int):
    user = request.state.user
    sensor = await Sensors.filter(Q(company_id=user.company_id) | Q(system_data=1), id=sensor_id, invalid=0).first()
    assert sensor, "传感器不存在"
    return sensor


@router.get(
    "/sensors",
    summary='获取传感器列表',
    tags=["Sensors"]
)
async def list_sensor(pagenum: int = 1, pagesize: int = 15, content: str = "", sensor_type: Optional[str] = None,
                      group_type: str = ""):
    user = request.state.user
    sensors_model = Sensors.filter(Q(company_id=user.company_id) | Q(system_data=1), invalid=0)

    if content:
        sensors_model = sensors_model.filter(Q(name__contains=content) | Q(desc__contains=content))
    if sensor_type:
        sensors_model = sensors_model.filter(type=sensor_type)
    if group_type:
        sensors_model = sensors_model.filter(group_type=group_type)

    total_num = await sensors_model.count()
    if pagesize == 0:
        res = await sensors_model.all()
    else:
        res = await sensors_model.limit(pagesize).offset(max(0, pagenum - 1) * pagesize).all()
    pageinfo = utils.utils.paginate(total_num, pagesize)
    res = sorted(res, key=lambda v: v.modified_at, reverse=True)
    return {'pageinfo': pageinfo, 'datas': res}
