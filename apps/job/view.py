import copy
import os
import json
import datetime
import time

from decimal import Decimal
from typing import List
from tortoise import transactions
from fastapi import APIRouter, status, Body, Depends, Request
from fastapi.encoders import jsonable_encoder
from tortoise.expressions import Q
from tortoise.functions import Max
from tortoise.transactions import in_transaction
from core.settings import TIMES
from core.middleware import limiter
from utils import utils
from .job_helper import *
from .schema import CreateJob, UpdateJob
from .model import Jobs
from ..auth.auth_casbin import AuthorityRole
from ..car.model import Cars, CarSensors
from ..controller.model import Controllers
from ..dynamic.model import Dynamics
from ..log.model import Logs
from ..scenario.model import Scenarios
from ..scenario.scenario_helper import json_convert_to_openscenario
from ..sensor.model import Sensors, SensorData
from ..task.model import Tasks
from utils.auth import request
from .job_helper import get_nodes_status
from .report_tool.report_helper import Report
from starlette.responses import FileResponse
from pathlib import Path

router = APIRouter()
rgb_for_replay = {
    "type": "sensor.camera.rgb",
    "id": "view",
    "role_name": "record_rgb",
    "spawn_point": {"x": -7, "y": 0, "z": 2, "roll": 0, "pitch": -15, "yaw": 0},
    "image_size_x": 800,
    "image_size_y": 600,
    "fov": 90,
    "sensor_tick": 0.05,
    "gamma": 2.2,
    "shutter_speed": 200,
    "iso": 100,
    "fstop": 8,
    "min_fstop": 1.2,
    "blade_count": 5,
    "exposure_mode": "histogram",
    "exposure_compensation": 0,
    "exposure_min_bright": 7,
    "exposure_max_bright": 9,
    "exposure_speed_up": 3,
    "exposure_speed_down": 1,
    "calibration_constant": 16,
    "focal_distance": 1000,
    "blur_amount": 1,
    "blur_radius": 0,
    "motion_blur_intensity": 0.45,
    "motion_blur_max_distortion": 0.35,
    "motion_blur_min_object_screen_size": 0.1,
    "slope": 0.88,
    "toe": 0.55,
    "shoulder": 0.26,
    "black_clip": 0,
    "white_clip": 0.04,
    "temp": 6500,
    "tint": 0,
    "chromatic_aberration_intensity": 0,
    "chromatic_aberration_offset": 0,
    "enable_postprocess_effects": "True",
    "lens_circle_falloff": 5,
    "lens_circle_multiplier": 0,
    "lens_k": -1,
    "lens_kcube": 0,
    "lens_x_size": 0.08,
    "lens_y_size": 0.08,
    "bloom_intensity": 0.675,
    "lens_flare_intensity": 0.1,
    "sensor_id": "default",
    "sensor_name": "default_cam",
    "nickname": "RGB相机"
}


@router.post(
    "/create_job",
    summary='创建作业',
    tags=["Job"]
)
@limiter.limit("%d/minute" %TIMES)
async def create_job(request: Request, job_create_model: CreateJob):
    """create a new job.
    car_id 和 scenario_ids 存入，后面直接查询对应的表，不要快照，同时生成task表，吧scenario信息存进去"""
    user = request.state.user
    assert not await Jobs.filter(Q(company_id=user.company_id) | Q(system_data=1), name=job_create_model.name,
                                 invalid=0).first(), '作业名称已存在'
    car_obj = await Cars.filter(Q(company_id=user.company_id) | Q(system_data=1), id=job_create_model.car_id,
                                invalid=0).first()
    assert car_obj, '主车信息不存在'
    car_sensor = await CarSensors.filter(car_id=job_create_model.car_id, invalid=0).first()
    assert car_sensor, '主车上没有添加传感器'
    sensor_obj = await Sensors.filter(Q(company_id=user.company_id) | Q(system_data=1), id=car_sensor.sensor_id,
                                      invalid=0).first()
    assert sensor_obj, '传感器信息不存在'
    scenario_infos = await Scenarios.filter(id__in=job_create_model.scenario_ids, company_id=user.company_id, invalid=0).all()
    assert len(scenario_infos) == len(job_create_model.scenario_ids), '场景存在异常，检查是否有无效场景'

    async with transactions.in_transaction():
        job = Jobs(**job_create_model.dict())
        job.status = "waiting"
        job.user_id = user.id
        job.company_id = user.company_id
        await job.save()
        job_id = job.id
        job_name = job.name
        task_snaps = []
        for scenario_id in job_create_model.scenario_ids:
            scenario = await Scenarios.filter(id=scenario_id, company_id=user.company_id, invalid=0).first()
            task_snap = Tasks()
            task_snap.desc = scenario.desc
            task_snap.user_id = user.id
            task_snap.job_id = job_id
            task_snap.company_id = user.company_id
            task_snap.job_name = job_name
            assert len(scenario.name) <= 64, "场景名称超过了64个字符"
            task_snap.name = scenario.name
            task_snap.scenario_id = scenario.id
            task_snap.scenario_tags = scenario.tags
            task_snap.status = "waiting"
            task_snaps.append(task_snap)

        await Tasks.bulk_create(task_snaps)
    return job_id


@router.put(
    "/update_job/{job_id}",
    summary='更新作业信息',
    tags=["Job"]
)
@limiter.limit("%d/minute" %TIMES)
async def update_job(request: Request, job_id: int, job_update_model: UpdateJob):
    """update job， 这个时候更新job表里面的所有信息，重新刷一遍保存；同时如果场景和主车发生改变，要将task表刷新，
    删掉的scenario变为无效，新增的添加到task"""
    user = request.state.user
    job_model = await Jobs.filter(Q(company_id=user.company_id) | Q(system_data=1), id=job_id, invalid=0).first()
    assert job_model, "作业不存在"
    if job_model.name != job_update_model.name:
        assert not await Jobs.filter(name=job_update_model.name, company_id=user.company_id, invalid=0).first(), \
            '作业名称已存在'
    assert job_model.status == "waiting", '作业状态错误'
    car_obj = await Cars.filter(Q(company_id=user.company_id) | Q(system_data=1), id=job_update_model.car_id,
                                invalid=0).first()
    assert car_obj, '主车信息不存在'
    car_sensor = await CarSensors.filter(car_id=job_update_model.car_id, invalid=0).first()
    assert car_sensor, '主车上没有添加传感器'
    sensor_obj = await Sensors.filter(Q(company_id=user.company_id) | Q(system_data=1), id=car_sensor.sensor_id,
                                      invalid=0).first()
    assert sensor_obj, '传感器信息不存在'

    scenario_infos = await Scenarios.filter(id__in=job_update_model.scenario_ids, invalid=0).all()
    assert len(scenario_infos) == len(job_update_model.scenario_ids), '场景存在异常，检查是否有无效场景'
    # 获取所有的 scenario id,删除掉前端删掉的任务
    task_all = await Tasks.filter(Q(company_id=user.company_id) | Q(system_data=1), job_id=job_id, invalid=0).all()
    assert task_all, "场景不存在，检查作业是否存在场景"

    async with transactions.in_transaction():
        if job_update_model.scenario_ids != job_model.scenario_ids:
            for t in task_all:
                await Tasks.filter(id=t.id).update(invalid=t.id)

            for scenario in scenario_infos:
                task_snap = Tasks()
                task_snap.desc = scenario.desc
                task_snap.job_id = job_id
                task_snap.job_name = job_update_model.name
                task_snap.name = scenario.name
                task_snap.scenario_id = scenario.id
                task_snap.scenario_tags = scenario.tags
                task_snap.status = "waiting"
                task_snap.user_id = user.id
                task_snap.company_id = user.company_id
                await task_snap.save()
        await job_model.update_from_dict(job_update_model.dict()).save()
    return


@router.get(
    "/job/{job_id}",
    summary='获取作业详细情',
    tags=["Job"]
)
async def get_job(job_id: int):
    """
    get job details;
    if status is waiting,return edit page info
    if status is not waiting, return detail info
    """
    user = request.state.user
    job_info = await Jobs.filter(Q(company_id=user.company_id) | Q(system_data=1), id=job_id, invalid=0).first()
    assert job_info, '任务不存在'
    status = job_info.status

    if status == "waiting":
        car_obj = await Cars.filter(Q(company_id=user.company_id) | Q(system_data=1), id=job_info.car_id,
                                    invalid=0).first()
        job_info.car_snap = car_obj if car_obj else []
        tasks = await Scenarios.filter(id__in=job_info.scenario_ids, invalid=0).all()
        if not tasks:
            job_info.scenario_ids = []
        # job_info.sensor_snap = sensor_obj
    else:
        tasks = await Tasks.filter(job_id=job_id, invalid=0, company_id=user.company_id).order_by("index").all()

    job_info = jsonable_encoder(job_info)
    controller_version = await Controllers.filter(id=job_info['controller_version'], invalid=0).first()
    job_info['controller_version_name'] = controller_version.version if controller_version else ''
    controller = await Controllers.filter(id=job_info['controller'], invalid=0).first()
    job_info['controller_name'] = controller.name if controller else ''
    job_info['tasks'] = jsonable_encoder(tasks) if tasks else []
    if status != "waiting":
        job_info = handle_finish_pass_job(job_info)
    return job_info


@router.get(
    "/job_detail/{job_id}",
    summary='获取主车信息',
    tags=["Job"]
)
async def get_car_info(job_id: int):
    """
    get job car snap details;
    """
    user = request.state.user
    job_info = await Jobs.filter(Q(company_id=user.company_id) | Q(system_data=1), id=job_id, invalid=0).first()
    assert job_info, '任务不存在'
    car_info = dict()
    car_info['car_snap'] = job_info.car_snap
    car_info['sensor_snap'] = job_info.sensors_snap
    return car_info


@router.delete(
    "/{job_ids}",
    summary='删除作业',
    tags=["Job"],
    dependencies=[Depends(AuthorityRole('admin'))]
)
@limiter.limit("%d/minute" %TIMES)
async def delete_job(request: Request, job_ids: str):
    job_id_list = job_ids.split(",")
    assert len(job_id_list) > 0, "未添加要删除作业id"
    user = request.state.user
    for job_id in job_id_list:
        job = await Jobs.filter(id=job_id, company_id=user.company_id, invalid=0).first()
        assert job, "作业不存在"
        assert job.status in ['waiting', 'finish'], "仅支持删除已完成和未运行状态作业"
        job.invalid = job_id
        await job.save()

        tasks = await Tasks.filter(id=job_id, company_id=user.company_id, invalid=0).all()
        if tasks:
            for task in tasks:
                task.invalid = task.job_id
            await Tasks.bulk_update(tasks, fields=['invalid'])
    return True


@router.delete(
    "/task_by_ids/{job_id}",
    summary='删除任务',
    tags=["Job"],
    dependencies=[Depends(AuthorityRole('admin'))]
)
@limiter.limit("%d/minute" %TIMES)
async def delete_task(request: Request, job_id: int, task_ids: List[int] = Body(..., embed=True)):
    user = request.state.user
    tasks = await Tasks.filter(job_id=job_id, id__in=task_ids, company_id=user.company_id, invalid=0).all()
    assert tasks, "任务不存在"
    assert len(tasks) == len(task_ids), '存在错误的任务id'

    for task in tasks:
        task.invalid = task.id
    await Tasks.bulk_update(tasks, fields=["invalid"])


@router.post(
    "/job_list",
    summary='获取作业列表',
    tags=["Job"]
)
async def get_job_list(pagenum: int = 1, pagesize: int = 15, asc: int = -1, status: List[str] = Body([], embed=True),
                       content: str = "", recent: str = "", rets: List[str] = Body([], embed=True)):
    user = request.state.user
    cond = []
    vcs = []

    if status:
        cond.append(' jobs.status in %s ')
        vcs += [tuple(status)]

    if content:
        cond.append(' ( jobs.name like %s or jobs.desc like %s ) ')
        vcs += ['%{}%'.format(content), '%{}%'.format(content)]

    if rets:
        cond.append(' tasks.ret_status in %s ')
        vcs += [tuple(rets)]

    if recent:
        time_str = filter_recent(recent)
        cond.append(' jobs.modified_at >= %s ')
        vcs += [time_str]

    cond.append(' jobs.invalid = 0 and jobs.company_id = %s or jobs.system_data = 1 ')
    vcs += [user.company_id]

    cond = ' and '.join(cond)

    async with in_transaction() as trans:
        data = await trans.execute_query(
            'select count(1) as total from jobs left join tasks on tasks.job_id = jobs.id where {} group by jobs.id,jobs.name,jobs.status '.format(
                cond if cond else 1), vcs)
        total_num = data[0]
        vcs += [pagesize, max(pagenum - 1, 0) * pagesize]
        sql = "select jobs.id as job_id," \
              "jobs.name as job_name," \
              "jobs.status as job_status," \
              "jobs.name_en as job_name_en," \
              "jobs.desc as job_desc," \
              "jobs.desc_en as job_desc_en," \
              "jobs.render_mode as render_mode," \
              "jobs.controller as controller," \
              "jobs.system_data as system_data," \
              "jobs.controller_version as controller_version," \
              "max(jobs.modified_at) as modified_at," \
              "count(tasks.id) as task_num," \
              "count(if(tasks.ret_status='pass',true,null)) as pass_num," \
              "count(if(tasks.ret_status='failure',true,null)) as failure_num," \
              "count(if(tasks.status='inqueue',true,null)) as inqueue_num," \
              "count(if(tasks.status='running',true,null)) as running_num," \
              "count(if(tasks.status='finish',true,null)) as finish_num," \
              "count(if(tasks.ret_status='exception',true,null)) as exception_num " \
              "from jobs left join tasks on tasks.job_id = jobs.id where {} group by jobs.id,jobs.name,jobs.status order by jobs.modified_at " + (
                  'desc' if asc == -1 else 'asc') + " limit %s offset %s"

        datas = await trans.execute_query(sql.format(cond), vcs)
        for data in datas[1]:
            data['modified_at'] = data['modified_at'].strftime("%Y-%m-%d %H:%M:%S")
    pageinfo = utils.paginate(total_num, pagesize)

    return {'pageinfo': pageinfo, 'datas': datas[1]}


@router.post(
    "/run_job/{job_id}",
    summary='运行作业',
    tags=["Job"]
)
async def run_job(job_id: int):
    user = request.state.user
    job_model = await Jobs.filter(Q(company_id=user.company_id) | Q(system_data=1), id=job_id, invalid=0,
                                  status="waiting").first()
    assert job_model, "作业不存在"
    task_snap = await Tasks.filter(Q(company_id=user.company_id) | Q(system_data=1), job_id=job_id, invalid=0,
                                   status="waiting").order_by('id').all()
    assert task_snap, "任务不存在"

    car_info = await Cars.filter(Q(company_id=user.company_id) | Q(system_data=1), id=job_model.car_id,
                                 invalid=0).first()
    assert car_info, '主车信息不存在'

    dynamic_info = await Dynamics.filter(Q(company_id=user.company_id) | Q(system_data=1), id=car_info.dynamics_id,
                                         invalid=0).first()
    assert dynamic_info, '动力学模型不存在'

    sensors_snap = await CarSensors.filter(car_id=car_info.id, invalid=0).all()
    assert sensors_snap, '主车上传感器不存在'
    controller = await Controllers.filter(id=job_model.controller, invalid=0).first()
    controller_version = await Controllers.filter(id=job_model.controller_version, invalid=0).first()
    assert controller, '控制系统不存在'
    assert controller_version, '控制系统版本不存在'
    sensors_list = []
    sensors_snap = jsonable_encoder(sensors_snap)
    for s in sensors_snap:
        sensor_info = await Sensors.filter(Q(company_id=user.company_id) | Q(system_data=1), id=s["sensor_id"]).first()
        # 判断camera sensor上若semantic、instance字段值为Ture则增加对应的sensor
        if "camera" in s["type"] and s["semantic"]:
            sensors_list.append({"type": "sensor.camera.semantic_segmentation",
                                 'car_sensor_id': s['id'],
                                 "semantic": s.get("semantic"),
                                 "spawn_point": {"x": s.get("position_x"),
                                                 "y": s.get("position_y"),
                                                 "z": s.get("position_z"),
                                                 "roll": s.get("roll"),
                                                 "pitch": s.get("pitch"),
                                                 "yaw": s.get("yaw"),
                                                 },
                                 "fov": sensor_info.param.get("fov"),
                                 "image_size_x": sensor_info.param.get("image_size_x"),
                                 "image_size_y": sensor_info.param.get("image_size_y"),
                                 "sensor_tick": sensor_info.param.get("sensor_tick")
                                 })
        if "camera" in s["type"] and s["instance"]:
            sensors_list.append({"type": "sensor.camera.instance_segmentation",
                                 'car_sensor_id': s['id'],
                                 "instance": s.get("instance"),
                                 "spawn_point": {"x": s.get("position_x"),
                                                 "y": s.get("position_y"),
                                                 "z": s.get("position_z"),
                                                 "roll": s.get("roll"),
                                                 "pitch": s.get("pitch"),
                                                 "yaw": s.get("yaw"),
                                                 },
                                 "fov": sensor_info.param.get("fov"),
                                 "image_size_x": sensor_info.param.get("image_size_x"),
                                 "image_size_y": sensor_info.param.get("image_size_y"),
                                 "sensor_tick": sensor_info.param.get("sensor_tick")
                                 })
        sensors_list.append({
            **{"type": s["type"], "name": s["name"], "data_record": s["data_record"], "car_sensor_id": s["id"],
               "semantic": s["semantic"], "instance": s["instance"], 'nick_name': s['nick_name']},
            **{
                "spawn_point": {
                    "x": s["position_x"],
                    "y": s["position_y"],
                    "z": s["position_z"],
                    "roll": s["roll"],
                    "pitch": s["pitch"],
                    "yaw": s["yaw"],
                }
            },
            **jsonable_encoder(sensor_info.param)})
        # sensors_list.append(rgb_for_replay)
    car_snap = jsonable_encoder(car_info)
    dynamic_info.param['dynamics_id'] = dynamic_info.id
    dynamic_info.param['dynamics_name'] = dynamic_info.name
    dynamic_info.param['dynamics_name_en'] = dynamic_info.name_en
    car_snap["vehicle_physics_control"] = jsonable_encoder(dynamic_info.param)

    queue_sess = request.app.state.redis
    index = 100
    async with transactions.in_transaction():
        sensor_data_snap = []
        for task in task_snap:
            scenario_param = await Scenarios.filter(id=task.scenario_id, invalid=0).first()
            assert scenario_param, '{}场景信息缺失,检查场景是否存在'.format(task.name)
            scenario_param = jsonable_encoder(scenario_param)
            try:
                openscenario, ego_start_postion, ego_target_postion = await json_convert_to_openscenario(
                    scenario_param, car_snap, request.state.user.id)
            except Exception as e:
                assert False, f'任务{task.name}场景格式转换失败'
            scenario_param.setdefault("dynamic_scene", {})
            scenario_param["dynamic_scene"]["scene_script"] = openscenario
            scenario_param["dynamic_scene"]["type"] = "openScenario"
            scenario_param["ego_start_and_end_position"] = {"start_position": ego_start_postion,
                                                            "end_position": ego_target_postion}
            task.scenario_param = scenario_param
            task.status = "inqueue"
            task.index = Decimal(index / 100)
            await task.save()
            new_sensors = []
            for num, sensor in enumerate(sensors_list):
                # 对sensors_list中的各个sensor添加role_name
                sensor["role_name"] = ".".join([str(task.id), sensor["type"], str(num)])
                if (sensor.get("data_record") or sensor.get("semantic") or sensor.get("instance")) \
                        and (("instance" not in sensor.get("type")) and ("semantic" not in sensor.get("type"))):
                    sensor_data_info = SensorData()
                    sensor_data_info.sensor_name = sensor["name"]
                    sensor_data_info.sensor_type = sensor["type"]
                    sensor_data_info.car_sensor_id = sensor["car_sensor_id"]
                    sensor_data_info.task_id = task.id
                    sensor_data_snap.append(sensor_data_info)
                if job_model.render_mode == 'norender':
                    if sensor.get('type') in ['sensor.camera.goal', 'sensor.lidar.goal']:
                        new_sensors.append(sensor)
                else:
                    new_sensors.append(sensor)

            task_info = jsonable_encoder(task)
            task_info['id'] = str(task_info['id'])
            task_info['job_id'] = str(task_info['job_id'])
            task_info['car_snap'] = car_snap
            task_info.setdefault('sensors_snap', {})
            task_info['sensors_snap'].setdefault('sensors', new_sensors)
            task_info['agent'] = controller_version.setup_file_name
            task_info['conf'] = controller_version.config_file_name
            task_info['data_flow'] = controller_version.data_flow_file_name
            task_info['view_record'] = job_model.view_record
            task_info['show_game_window'] = job_model.show_game_window
            dic = {"action": "RUN", "task": task_info}

            assert task_info['scenario_param']["evaluation_standard"], "evaluation_standard not exits"
            await queue_sess.hset('task_infos', task.id, json.dumps(dic))
            index += 100
            sensor_cam_info = SensorData()
            sensor_cam_info.task_id = task.id
            sensor_cam_info.sensor_name = "record_rgb"
            sensor_cam_info.sensor_type = "sensor.camera.rgb"
            sensor_cam_info.car_sensor_id = 0
            sensor_data_snap.append(sensor_cam_info)
        await SensorData.bulk_create(sensor_data_snap)
        job_model.car_snap = car_snap
        job_model.sensors_snap = sensors_snap
        job_model.status = "inqueue"
        job_model.start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        await job_model.save()
        return "执行成功"


@router.post(
    "/create_and_run_new_job",
    summary='创建并运行新的作业',
    tags=["Job"]
)
async def create_and_run_new_job(request: Request, job_create_model: CreateJob):
    job_id = await create_job(request, job_create_model)
    await run_job(job_id)
    return job_id


@router.post(
    "/stop_jobs",
    summary='终止作业',
    tags=["Job"]
)
async def stop_jobs(job_ids: List[int] = Body(..., embed=True)):
    user = request.state.user
    jobs = await Jobs.filter(Q(company_id=user.company_id) | Q(system_data=1), id__in=job_ids, invalid=0).all()
    assert jobs, "作业不存在"
    task_snap = await Tasks.filter(Q(company_id=user.company_id) | Q(system_data=1), job_id__in=job_ids,
                                   invalid=0).all()
    assert task_snap, "任务不存在"

    async with transactions.in_transaction():
        for task in task_snap:
            await task.update_from_dict({'status': 'waiting', 'start_time': None, 'end_time': None}).save()
            sensor_data_item = await SensorData.filter(task_id=task.id, invalid=0).all()
            for data_item in sensor_data_item:
                data_item.modified_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                await data_item.update_from_dict({"invalid": task.id}).save()
        for job in jobs:
            job.modified_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            await job.update_from_dict({'status': 'waiting', 'start_time': None, 'end_time': None}).save()
    return


@router.post(
    "/retry_task",
    summary='重试任务',
    tags=["Job"]
)
async def retry_task(job_id: str, task_ids: List[int] = Body(..., embed=True)):
    user = request.state.user
    job_model = await Jobs.filter(Q(company_id=user.company_id) | Q(system_data=1), id=job_id, invalid=0).first()
    assert job_model, "作业不存在"
    task_snap = await Tasks.filter(Q(company_id=user.company_id) | Q(system_data=1), job_id=job_id, invalid=0,
                                   id__in=task_ids).all()
    assert task_snap, "任务不存在"

    queue_sess = request.app.state.redis
    controller = await Controllers.filter(id=job_model.controller, invalid=0).first()
    controller_version = await Controllers.filter(id=job_model.controller_version, invalid=0).first()
    assert controller, '控制系统不存在'
    assert controller_version, '控制系统版本不存在'
    async with transactions.in_transaction():
        sensor_data_snap = []
        for t in task_snap:
            now_max_index = await Tasks.filter(invalid=0,
                                               job_id=job_id,
                                               index__gte=t.index,
                                               index__lt=int(t.index) + 1) \
                .annotate(max_index=Max('index')).first().values('max_index')
            now_max_index = now_max_index['max_index']
            task = Tasks()
            task.status = "inqueue"
            task.end_time = None
            task.scenario_id = t.scenario_id
            task.job_id = t.job_id
            task.job_name = t.job_name
            task.scenario_param = t.scenario_param
            task.scenario_tags = t.scenario_tags
            task.user_id = t.user_id
            task.company_id = t.company_id
            task.desc = t.desc
            task.index = Decimal((now_max_index * 100 + 1) / 100).quantize(Decimal('0.00'))
            ori_task = await Tasks.filter(invalid=0, job_id=job_id, scenario_id=t.scenario_id,
                                          index=int(t.index)).first()
            if str(task.index) == '01':
                task.name = t.name + '_' + str(task.index).split(".")[-1]
            else:
                task.name = ori_task.name + '_' + str(task.index).split(".")[-1]
            task.result = {}
            await task.save()

            sensors_list = []
            sensors_snap = job_model.sensors_snap
            for s in sensors_snap:
                sensor_info = await Sensors.filter(Q(company_id=user.company_id) | Q(system_data=1),
                                                   id=s['sensor_id']).first()
                # 判断camera sensor上若semantic、instance字段值为Ture则增加对应的sensor
                if "camera" in s["type"] and s["semantic"]:
                    sensors_list.append({"type": "sensor.camera.semantic_segmentation",
                                         "semantic": s.get("semantic"),
                                         'car_sensor_id': s['id'],
                                         "spawn_point": {"x": s.get("position_x"),
                                                         "y": s.get("position_y"),
                                                         "z": s.get("position_z"),
                                                         "roll": s.get("roll"),
                                                         "pitch": s.get("pitch"),
                                                         "yaw": s.get("yaw"),
                                                         },
                                         "fov": sensor_info.param.get("fov"),
                                         "image_size_x": sensor_info.param.get("image_size_x"),
                                         "image_size_y": sensor_info.param.get("image_size_y"),
                                         "sensor_tick": sensor_info.param.get("sensor_tick")
                                         })
                if "camera" in s["type"] and s["instance"]:
                    sensors_list.append({"type": "sensor.camera.instance_segmentation",
                                         "instance": s.get("instance"),
                                         'car_sensor_id': s['id'],
                                         "spawn_point": {"x": s.get("position_x"),
                                                         "y": s.get("position_y"),
                                                         "z": s.get("position_z"),
                                                         "roll": s.get("roll"),
                                                         "pitch": s.get("pitch"),
                                                         "yaw": s.get("yaw"),
                                                         },
                                         "fov": sensor_info.param.get("fov"),
                                         "image_size_x": sensor_info.param.get("image_size_x"),
                                         "image_size_y": sensor_info.param.get("image_size_y"),
                                         "sensor_tick": sensor_info.param.get("sensor_tick")
                                         })
                sensors_list.append({**{'type': s['type'], 'name': s['name'], 'data_record': s['data_record'],
                                        'car_sensor_id': s['id'], "semantic": s["semantic"], "instance": s["instance"],
                                        'nick_name': s['nick_name']},
                                     **{
                                         'spawn_point': {
                                             "x": s['position_x'],
                                             "y": s['position_y'],
                                             "z": s['position_z'],
                                             "roll": s['roll'],
                                             "pitch": s['pitch'],
                                             "yaw": s['yaw'],
                                         }
                                     }, **jsonable_encoder(sensor_info.param)})
                # sensors_list.append(rgb_for_replay)
            new_sensors = []
            for num, sensor in enumerate(sensors_list):
                # 对sensors_list中的各个sensor添加role_name
                sensor["role_name"] = ".".join([str(task.id), sensor["type"], str(num)])
                new_sensors.append(sensor)
                if (sensor.get("data_record") or sensor.get("semantic") or sensor.get("instance")) \
                        and (("instance" not in sensor.get("type")) and ("semantic" not in sensor.get("type"))):
                    sensor_data_info = SensorData()
                    sensor_data_info.sensor_name = sensor["name"]
                    sensor_data_info.sensor_type = sensor["type"]
                    sensor_data_info.car_sensor_id = sensor["car_sensor_id"]
                    sensor_data_info.task_id = task.id
                    sensor_data_snap.append(sensor_data_info)

            sensor_cam_info = SensorData()
            sensor_cam_info.task_id = task.id
            sensor_cam_info.sensor_name = "record_rgb"
            sensor_cam_info.sensor_type = "sensor.camera.rgb"
            sensor_cam_info.car_sensor_id = 0
            sensor_data_snap.append(sensor_cam_info)

            task_info = jsonable_encoder(task)
            task_info['id'] = str(task_info['id'])
            task_info['job_id'] = str(task_info['job_id'])
            task_info['car_snap'] = job_model.car_snap
            task_info['agent'] = controller_version.setup_file_name
            task_info['conf'] = controller_version.config_file_name
            task_info['data_flow'] = controller_version.data_flow_file_name
            task_info.setdefault('sensors_snap', {})
            task_info['sensors_snap'].setdefault('sensors', new_sensors)
            task_info['view_record'] = job_model.view_record
            task_info['show_game_window'] = job_model.show_game_window
            dic = {"action": "RUN", "task": task_info}

            assert task_info['scenario_param']["evaluation_standard"], "evaluation_standard not exits"
            await queue_sess.hset('task_infos', task.id, json.dumps(dic))

        await SensorData.bulk_create(sensor_data_snap)
        job_model.modified_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        job_model.status = "running"
        await job_model.save()


@router.get(
    "/total_task_info",
    summary='获取总的任务信息',
    tags=["Job"]
)
async def get_total_task_info():
    ret_dic = {}
    failure_num = 0
    passed_num = 0
    exception_num = 0
    runing_num = 0
    waiting_num = 0
    finished_num = 0
    queue_num = 0

    user = request.state.user
    jobs = await Jobs.filter(company_id=user.company_id, invalid=0).all()
    for job_model in jobs:
        task_snap = await Tasks.filter(company_id=user.company_id, invalid=0, job_id=job_model.id).all()
        for task in task_snap:
            if task.status == "inqueue":
                queue_num += 1
            if task.status == "finish":
                finished_num += 1
            if task.status == "waiting":
                waiting_num += 1
            if task.status == "running":
                runing_num += 1
            if task.ret_status == "exception":
                exception_num += 1
                continue
            if task.ret_status == "failure":
                failure_num += 1
                continue
            if task.ret_status == "pass":
                passed_num += 1
    queue_sess = request.app.state.redis
    free_num = await queue_sess.hget('node_status', 'free_num')
    busy_num = await queue_sess.hget('node_status', 'busy_num')
    exct_num = await queue_sess.hget('node_status', 'exct_num')
    free_nodes_num = int(free_num) if free_num else 0
    busy_nodes_num = int(busy_num) if busy_num else 0
    exct_nodes_num = int(exct_num) if exct_num else 0
    ret_dic["queue_num"] = queue_num
    ret_dic["failure_num"] = failure_num
    ret_dic["passed_num"] = passed_num
    ret_dic["exception_num"] = exception_num
    ret_dic["finished_num"] = finished_num
    ret_dic["waiting_num"] = waiting_num
    ret_dic["runing_num"] = runing_num
    ret_dic["free_nodes_num"] = free_nodes_num
    ret_dic["busy_nodes_num"] = busy_nodes_num
    ret_dic["exct_nodes_num"] = exct_nodes_num
    ret_dic["error_nodes_num"] = 0

    return ret_dic


@router.get(
    "/task_info",
    summary='获取任务详情',
    tags=["Job"]
)
async def get_task_info(task_id: int):
    user = request.state.user
    task = await Tasks.filter(id=task_id, company_id=user.company_id, invalid=0).first()
    assert task, "任务不存在"
    assert task.status in ['timeout', 'finish'], "仅支持已完成状态任务信息查询"
    job = await Jobs.filter(id=task.job_id, company_id=user.company_id, invalid=0).first()
    assert job, "作业信息不存在"
    ret_dic = {}
    task_dic = jsonable_encoder(task)
    task_dic["show_game_window"] = job.show_game_window
    task_dic["view_record"] = job.view_record
    timer, task_dic['running_time'] = cal_running_time(task_dic['start_time'], task_dic['end_time'])
    car_info = await assember_car_info(job)
    ret_dic.update(car_info)
    record_data_sensors = record_data_sensor_list(job)
    ret_dic.update(record_data_sensors)
    if task.result:
        car_event_list = handle_car_event(task.result.get("criteria", []))
        ret_list = sort_criteria(task_dic.get('result').get('criteria'))
        task_dic['result']['criteria'] = ret_list
    else:
        car_event_list = []
        evaluat_list = handel_evaluation(task)
        ret_dic.update({'evaluat_list': evaluat_list})
    ret_dic.update({"task": task_dic})
    ret_dic.update({'car_event_list': car_event_list})
    logs = await Logs.filter(task_id=task_id, type='').all()
    for lo in logs:
        if lo.game_time:
            try:
                time_str = str(round(float(lo.game_time), 2))
                lo.game_time = "%.2d:%.2d.%s" % (int(time_str.split(".")[0]) // 60, int(time_str.split(".")[0]) % 60,
                                                 time_str.split(".")[1])
            except:
                print('格式化失败')
    logs.sort(key=lambda log: (log.created_at, log.id))
    scenario_logs = await Logs.filter(task_id=task_id, type="scenario").all()
    for log in scenario_logs:
        log.msg = json.loads(log.msg)
        if log.msg.get('current_game_time') or log.msg.get("finish_game_time"):
            handel_game_time(log.msg, 'current_game_time')
    scenario_logs.sort(key=lambda log: log.created_at)
    ret_dic.update({"scenario_event_list": scenario_logs})
    controller = await Controllers.filter(id=job.controller, invalid=0).first()
    controller_version = await Controllers.filter(id=job.controller_version, invalid=0).first()
    ret_dic.update({"controller": controller.name if controller else '',
                    "controller_version": controller_version.version if controller_version else '',
                    "log_info": logs, "render_mode": job.render_mode})
    return ret_dic


@router.get(
    "/task_scenario_infos",
    summary='获取任务场景信息',
    tags=["Job"]
)
async def get_task_scenario_infos(task_id: int):
    user = request.state.user
    task = await Tasks.filter(id=task_id, company_id=user.company_id, invalid=0).first()
    assert task, "任务不存在"
    assert task.status in ['timeout', 'finish'], "仅支持已完成状态任务信息查询"
    task_dic = jsonable_encoder(task)
    return task_dic.get('scenario_param')


@router.get(
    "/job_report/{job_id}",
    summary='获取作业测试报告',
    tags=["Job"]
)
async def get_job_report(job_id: int, locale: str):
    """
    获取测试报告的接口
    params: 作业ID
    return: FileObject
    """
    job_info = await get_job(job_id)
    assert job_info["status"] == "finish", "仅提供完成状态的作业测试报告"
    try:
        # 作业信息 ["作业名称"，"测试主车", "受测系统", "测试环境", "开始时间", "结束时间"]
        # 结果汇总 ["场景总数", "通过", "失败", "无效", "总测试里程", "平均得分", "通过率"]
        job_info_desc, job_res_summary = get_job_info_desc(job_info, locale)

        # 获取任务详情数据 ["No.", "场景名称", "测试里程", "仿真时长", "任务结果", "评价通过率"]
        task_datas_list = get_task_detail_info(job_info, locale)

        # 调用report类函数生成报告
        report_name = "{}_{}_{}.pdf".format(job_info["name"], job_id, time.strftime("%Y%m%d-%H%M%S"))
        report_path = os.path.join('/tmp/', report_name)
        report = Report(job_info_desc, job_res_summary, task_datas_list, report_path, report_name, locale)
        report_path = report.create_file()
        print(report_path)
        return FileResponse(report_path, filename=Path(report_path).name)
    except Exception as e:
        assert False, "{}生成测试报告失败".format(job_info["name"])


@router.get(
    "/sensor_data",
    summary='获取传感器数据',
    tags=["Job"]
)
async def get_sensor_data(task_id: int, sensor_id: int, data_type: str):
    """
    获取传感器数据接口
    params: task_id sensor_id
    return: {}
    """
    sensor_data = await SensorData.filter(task_id=task_id, car_sensor_id=sensor_id, invalid=0).first()
    assert sensor_data, "传感器数据不存在"
    sensor_data = jsonable_encoder(sensor_data)
    if "camera" in sensor_data["sensor_type"]:
        if data_type == 'semantic':
            sensor_data["status"] = 'empty' if (sensor_data["process_rate_semantic"] == -1 or
                                                sensor_data["process_rate_semantic"] is None) else \
                ('data' if sensor_data["process_rate_semantic"] == 100 else 'loading')
        elif data_type == 'instance':
            sensor_data["status"] = 'empty' if (sensor_data["process_rate_instance"] == -1 or
                                                sensor_data["process_rate_instance"] is None) else \
                ('data' if sensor_data["process_rate_instance"] == 100 else 'loading')
        elif data_type == 'origin':
            sensor_data["status"] = 'empty' if (sensor_data["process_rate_img"] == -1 or
                                                sensor_data["process_rate_video"] == -1 or
                                                sensor_data["process_rate_img"] is None or
                                                sensor_data["process_rate_video"] is None) else \
                ('video' if (sensor_data["process_rate_img"] == 100 and sensor_data[
                    "process_rate_video"] == 100) else 'loading')
    elif "lidar" in sensor_data["sensor_type"] and sensor_data["data_url"]:
        sensor_data["status"] = "data"
    elif ("lidar" in sensor_data["sensor_type"] and (
            sensor_data["process_rate_data"] == -1 or sensor_data["process_rate_data"] is None)) or (
            "camera" in sensor_data["sensor_type"] and (
            sensor_data["process_rate_img"] == -1 or sensor_data["process_rate_img"] is None or
            sensor_data["process_rate_video"] == -1 or sensor_data["process_rate_video"] is None or
            sensor_data["process_rate_semantic"] == -1 or sensor_data["process_rate_semantic"] is None or
            sensor_data["process_rate_instance"] == -1 or sensor_data["process_rate_instance"] is None)):
        sensor_data["status"] = "empty"
    else:
        sensor_data["status"] = "loading"
    return sensor_data
