import datetime
import json

from apps.car.model import Cars, CarSensors
from apps.dynamic.model import Dynamics
from utils.auth import request
from tortoise.expressions import Q
from fastapi.encoders import jsonable_encoder
import etcd3
import os
from time import strftime
from time import gmtime


def timedelta_to_str(timedelta):
    hour = timedelta.seconds // 3600
    minute = timedelta.seconds // 60 % 60
    second = timedelta.seconds - hour * 3600 - minute * 60

    if hour < 10:
        hour_str = '0' + str(hour)
    else:
        hour_str = str(hour)

    if minute < 10:
        minute_str = '0' + str(minute)
    else:
        minute_str = str(minute)

    if second < 10:
        second_str = '0' + str(second)
    else:
        second_str = str(second)

    return hour_str + ":" + minute_str + ":" + second_str


def cal_running_time(start_time, end_time):
    if not start_time or not end_time:
        return None, ""
    try:
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        timedelta = end_time - start_time
        timedelta_str = timedelta_to_str(timedelta)
        return timedelta, timedelta_str
    except:
        return None, ""


def handle_finish_pass_job(job_task):
    pass_count = 0
    failure_count = 0
    invalid_count = 0
    inqueue_count = 0
    running_count = 0
    finish_count = 0
    exception_count = 0
    mileage_all = 0
    game_time_duration_all = 0.0
    for task in job_task["tasks"]:
        if task['status'].lower() in ['inqueue']:
            inqueue_count += 1
        elif task['status'].lower() in ['running']:
            running_count += 1
        elif task['status'].lower() in ['finish']:
            finish_count += 1
            if task.get('result'):
                game_time_duration_all += int(task.get("result", {}).get('summary', {}).get('game_time_duration', 0))
        else:
            exception_count += 1
        if task.get('result'):
            criterion_dict = dict()
            for item in task.get("result").get('criteria'):
                if item.get('name') in ['DrivenDistanceTest']:
                    task["mileage"] = item.get("actual_value", 0)
                    continue
                criterion_dict[item['name']] = item
            task['result']['list'] = criterion_dict
        if task.get('mileage'):
            mileage_all += task['mileage']
        if task.get("ret_status") == "failure":
            failure_count += 1
        elif task.get('ret_status') == "pass":
            pass_count += 1
        elif task.get('ret_status') == "exception":
            invalid_count += 1

    if job_task['status'] in ['finish', 'timeout']:
        timedelta_all, timedelta_str = cal_running_time(job_task['start_time'], job_task['end_time'])
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timedelta_all, timedelta_str = cal_running_time(job_task['start_time'], now)

    mile = mileage_all
    job_task['mileage'] = round(mileage_all, 1) if mile > 0 else ""
    job_task['game_time_duration_all'] = game_time_duration_all
    job_task['running_time'] = 0
    if timedelta_all:
        cost_time_str = timedelta_to_str(timedelta_all)
        job_task['running_time'] = cost_time_str if cost_time_str not in ["00:00:00"] else 0
    job_task['pass_count'] = pass_count
    job_task['failure_count'] = failure_count
    job_task['invalid_count'] = invalid_count
    job_task['inqueue_count'] = inqueue_count
    job_task['running_count'] = running_count
    job_task['finish_count'] = finish_count
    job_task['exception_count'] = exception_count
    return job_task


def filter_recent(recent):
    now = datetime.datetime.now()
    if recent == "day":
        day_start = datetime.datetime(now.year, now.month, now.day)
        return datetime.datetime.strftime(day_start, '%Y-%m-%d %H:%M:%S')
    elif recent == "week":
        day_start = datetime.datetime(now.year, now.month, now.day)
        week_start = day_start - datetime.timedelta(days=now.weekday())
        return datetime.datetime.strftime(week_start, '%Y-%m-%d %H:%M:%S')
    elif recent == "month":
        month_start = datetime.datetime(now.year, now.month, 1)
        return datetime.datetime.strftime(month_start, '%Y-%m-%d %H:%M:%S')


async def assember_car_info(job_info):
    car_info = job_info.car_snap
    car_info['dynamics_name'] = car_info.get('vehicle_physics_control').get('dynamics_name')
    car_info['dynamics_name_en'] = car_info.get('vehicle_physics_control').get('dynamics_name_en')
    car_info.pop('vehicle_physics_control')
    sensors = {"radar": [], "lidar": [], "imu": [], "gnss": [], "camera": [], "goal": [], 'ultrasonic': []}
    if job_info.sensors_snap:
        for sensor in job_info.sensors_snap:
            if sensor["type"] == "sensor.other.imu":
                sensors["imu"].append(sensor)
            elif sensor["type"] == "sensor.other.ultrasonic":
                sensors["ultrasonic"].append(sensor)
            elif sensor["type"] in ["sensor.lidar.ray_cast", 'sensor.lidar.ray_cast_mems']:
                sensors["lidar"].append(sensor)
            elif sensor["type"] == "sensor.other.gnss":
                sensors["gnss"].append(sensor)
            elif sensor["type"] == "sensor.other.radar":
                sensors["radar"].append(sensor)
            elif sensor["type"] in ['sensor.camera.depth', 'sensor.camera.rgb', "sensor.camera.fisheye"]:
                sensors["camera"].append(sensor)
            elif sensor["type"] in ['sensor.camera.goal', 'sensor.lidar.goal']:
                sensors["goal"].append(sensor)
            elif sensor["type"] in ['sensor.camera.goal', 'sensor.lidar.goal']:
                sensors["goal"].append(sensor)
    return {"car": car_info, "sensors": sensors}


name_map = {"ReachDestinationTest": '到达终点', "CollisionTest": '碰撞', "RunRedLightTest": '闯红灯',
            "RoadSpeedLimitTest": '超速', "OnRoadTest": '驶出行车道', "OntoSolidLineTest": '压实线',
            "MaxVelocityTest": '最高速度', "MinVelocityTest": '最低速度', "MaxAverageVelocityTest": '最高平均速度',
            "MinAverageVelocityTest": '最低平均速度', "AccelerationLongitudinalTest": '纵向加速度',
            "AccelerationLateralTest": '横向加速度', "AccelerationVerticalTest": '垂直加速度',
            "JerkLongitudinalTest": '纵向加速度变化率', "JerkLateralTest": '横向加速度变化率',
            'DrivenDistanceTest': "行驶里程"
            }


def sort_criteria(criteria_list):
    array_names = list(name_map.keys())
    ret_list = []
    for name in array_names:
        for criteria in criteria_list:
            if name == criteria.get('name'):
                ret_list.append(criteria)
    return ret_list


def handle_car_event(result_list):
    event_list = []
    for item in result_list:
        if not item.get("ego_event_list"):
            continue
        for dic in item.get('ego_event_list'):
            dic['name'] = item.get('name')
            dic['c_name'] = name_map.get(item.get('name'))
            if dic.get('game_time'):
                handel_game_time(dic, 'game_time')
            event_list.append(dic)
    return event_list


def handel_game_time(log_dict, key):
    try:
        if key == "current_game_time":
            key = "current_game_time" if log_dict.get("current_game_time") else "finish_game_time"
        time_str = str(round(log_dict.get(key), 2))
        log_dict[key] = "%.2d:%.2d.%s" % (
            int(time_str.split(".")[0]) // 60, int(time_str.split(".")[0]) % 60, time_str.split(".")[1])
    except:
        print('格式化失败')


def handel_evaluation(task):
    evaluate_list = []
    evaluation_standard = task.scenario_param.get('evaluation_standard', {})
    for key, eva in evaluation_standard.items():
        if isinstance(eva, dict):
            for k, v in eva.items():
                if "Test" in k:
                    evaluate_list.append({"name": k})
        else:
            evaluate_list.append({"name": key})
    array_names = list(name_map.keys())
    ret_list = []
    for name in array_names:
        for criteria in evaluate_list:
            if name == criteria.get('name'):
                ret_list.append(criteria)
    return ret_list


# from pathlib import Path
# from dotenv import load_dotenv


def get_nodes_status(status: bool):
    etcd_client = etcd3.client(host=os.environ.get('ETCD_HOST'), port=os.environ.get('ETCD_PORT'))
    keys = {}
    # ips = {}
    free_num = 0
    busy_num = 0

    carlas = etcd_client.get_prefix('/oasis/carlas')
    css = []
    for c in carlas:
        value, meta = c
        key = meta.key.decode()
        css.append(key)

    cs = [c for c in css if c + '/task' not in css]

    for e in cs:
        # value, meta = e
        # key = meta.key.decode()
        key = e
        # ips.setdefault(key.split("/")[3], {})
        keys.setdefault(key.split("/")[3], [])
        free_status = {
            'server_name': key.split("/")[4],
            'status': True  # free status
        }
        busy_status = {
            'server_name': key.split("/")[4],
            'status': False  # busy status
        }
        if key.split("/")[-1] != 'task':
            keys[key.split("/")[3]].append(free_status)
            free_num += 1
        else:
            keys[key.split("/")[3]].append(busy_status)
            busy_num += 1
    if status:
        return free_num
    else:
        return busy_num


def get_job_info_desc(job_info, locale="zh"):
    """
    获取生成测试报告所需的job作业信息、结果汇总信息
    params: job_info 当前作业信息
    return: [job_info_desc],【job_res_summary】
    """
    # 作业信息 ["作业名称"，"测试主车", "受测系统", "测试环境", "开始时间", "结束时间"]
    car_name_map = {"比赛车辆": "Contest Vehicle"}
    car_name = car_name_map[job_info["car_snap"]["name"]] if (locale == "en" and job_info["car_snap"]["name"] in car_name_map) else job_info["car_snap"]["name"]
    job_name = job_info["name_en"] if (locale == "en" and job_info["system_data"]) else job_info["name"]
    job_info_desc = [job_name, car_name,
                     job_info["controller_name"], job_info["controller_version_name"],
                     job_info["start_time"], job_info["end_time"]
                     ]
    # summary of results ["场景总数", "通过", "失败", "无效", "总测试里程", "平均得分", "通过率"]
    total_task_num = int(len(job_info["tasks"]))
    pass_task_num = int(job_info["pass_count"])
    failure_task_num = int(job_info["failure_count"])
    invalid_task_num = int(job_info["invalid_count"])
    total_mileage = "--"
    if job_info["mileage"]:
        total_mileage = "{}m".format(round(float(job_info["mileage"]), 1)) if float(job_info["mileage"]) < 1000 else \
            "{}km".format(round(job_info["mileage"] / 1000, 3))
    # 获取通过的task的平均得分
    total_score = 0
    for task in job_info["tasks"]:
        if task["result"]:
            total_score += float(task["result"]["summary"]["score"])
    average_score = round(total_score / total_task_num, 2)
    pass_rate = "{:.2%}".format(pass_task_num / total_task_num)
    job_res_summary = [total_task_num, pass_task_num,
                       failure_task_num, invalid_task_num,
                       total_mileage, average_score, pass_rate]
    return job_info_desc, job_res_summary


def get_task_detail_info(job_info, language="zh"):
    """
    获取生成测试报告中所需的任务详情的信息
    params: job_info 当前作业信息
    return: [task_info]
    """
    task_datas_list = []
    for task in job_info["tasks"]:
        task_evaluation_rate = ""
        task_res = ""
        task_run_time = strftime("%H:%M:%S", gmtime(float(task.get("result").get(
            "summary").get("game_time_duration")))) if task.get("result") else "--"
        task_test_mileage = "--"
        if task["mileage"]:
            task_test_mileage = "{}m".format(round(float(task["mileage"]), 1)) if float(task["mileage"]) < 1000 else \
                "{}km".format(round(float(task["mileage"]) / 1000, 3))
        if language == "en":
            task_execute_state = "finish" if task["status"] == "finish" else (
                "exception" if task["status"] == "timeout" else "--")
        else:
            task_execute_state = "完成" if task["status"] == "finish" else (
                "异常" if task["status"] == "timeout" else "--")
        if task["ret_status"] == "exception":
            task_res = "invalid" if language == "en" else "无效"
            task_evaluation_rate = calculate_task_evaluation_pass_num(task)
        elif task["ret_status"] == "failure":
            task_res = "failed" if language == "en" else "失败"
            task_evaluation_rate = calculate_task_evaluation_pass_num(task)
        elif task["ret_status"] == "pass":
            task_res = "pass" if language == "en" else "通过"
            task_evaluation_rate = calculate_task_evaluation_pass_num(task)
        if len(task["name"].encode()) > 72:
            task["name"] = "".join([task["name"][:30], "..."])
        # task["index"] = int(task["index"]) if len(str(task["index"]).split('.')[1]) == 1 else task["index"]
        task["index"] = int(task["index"]) if str(task["index"]).endswith('0') else task["index"]
        scenario_id = task["scenario_id"] if task.get("scenario_id") else "--"
        data_list = [task["index"], task["name"], scenario_id, task_execute_state, task_test_mileage,
                     task_run_time, task_res, task_evaluation_rate]
        task_datas_list.append(data_list)
    return task_datas_list


def calculate_task_evaluation_pass_num(task: dict):
    """
    合并结算task评价的通过项
    params: task 作业中的具体任务
    return: str eg:"8/10"
    """

    test_list = ['ReachDestinationTest', 'CollisionTest', 'RunRedLightTest', 'RoadSpeedLimitTest', 'OnRoadTest',
                 'OntoSolidLineTest', 'MaxVelocityTest',
                 'MinVelocityTest', 'MaxAverageVelocityTest', 'MinAverageVelocityTest', 'AccelerationLongitudinalTest',
                 'AccelerationLateralTest', 'AccelerationVerticalTest', 'JerkLongitudinalTest', 'JerkLateralTest']
    pass_num_dic = {}
    if task.get("result"):
        criterion_dict = dict()
        for item in task.get("result").get('criteria'):
            criterion_dict[item['name']] = item
        res_dict = criterion_dict
        for item in task["result"]["criteria"]:
            if item["name"] == 'MaxVelocityTest':
                if item["level"] == "poor" or res_dict["MinVelocityTest"]["level"] == "poor":
                    pass_num_dic["VelocityTest"] = 0
                else:
                    pass_num_dic["VelocityTest"] = 1
            elif item["name"] == 'MaxAverageVelocityTest':
                if item["level"] == "poor" or res_dict["MinAverageVelocityTest"]["level"] == "poor":
                    pass_num_dic["AverageVelocityTest"] = 0
                else:
                    pass_num_dic["AverageVelocityTest"] = 1
            elif item["name"] in test_list and (item["name"] not in ['MinVelocityTest', 'MinAverageVelocityTest']):
                pass_num_dic[item["name"]] = 1 if item["level"] != "poor" else 0
        task_evaluation_rate = "{}/{}".format(sum(pass_num_dic.values()), len(pass_num_dic.keys()))
        return task_evaluation_rate
    else:
        return "--"


def sensor_add_role_name(sensors_snap):
    for num, sensor in enumerate(sensors_snap):
        sensor["role_name"] = ".".join([sensor["type"], str(num)])
    return sensors_snap


def record_data_sensor_list(job_info):
    sensors = []
    if job_info.sensors_snap:
        for sensor in job_info.sensors_snap:
            if sensor["type"] == "sensor.other.imu" and sensor["data_record"]:
                sensor["group_type"] = "imu"
                sensors.append(sensor)
            elif sensor["type"] == "sensor.other.ultrasonic" and sensor["data_record"]:
                sensor["group_type"] = "ultrasonic"
                sensors.append(sensor)
            elif sensor["type"] in ["sensor.lidar.ray_cast", 'sensor.lidar.ray_cast_mems'] and sensor["data_record"]:
                sensor["group_type"] = "lidar"
                sensors.append(sensor)
            elif sensor["type"] == "sensor.other.gnss" and sensor["data_record"]:
                sensor["group_type"] = "gnss"
                sensors.append(sensor)
            elif sensor["type"] == "sensor.other.radar" and sensor["data_record"]:
                sensor["group_type"] = "radar"
                sensors.append(sensor)
            elif sensor["type"] in ['sensor.camera.depth', 'sensor.camera.rgb', "sensor.camera.fisheye"] and (
                    sensor["data_record"] or sensor["semantic"] or sensor["instance"]):
                sensor["group_type"] = "camera"
                sensors.append(sensor)
            # elif sensor["type"] in ['sensor.speedometer']:
            #     sensor["group_type"] = "speedometer"
            #     sensors.append(sensor)
            # elif sensor["type"] in ['sensor.opendrive_map']:
            #     sensor["group_type"] = "opendrive_map"
            #     sensors.append(sensor)
    return {"record_data_sensors": sensors}
