import json

from tortoise import transactions

from apps.dynamic.model import Dynamics
from apps.sensor.model import Sensors
from apps.car.model import Cars, CarSensors
from apps.job.model import Jobs
from apps.scenario.model import Scenarios
from apps.scenario.scenario_helper import upload_scenario
from apps.task.model import Tasks
from seeds.sensors_seeder import cam_list


async def seed_data(user):
    async with transactions.in_transaction():

        job = Jobs()
        job.name = "渲染模式预置场景"
        job.desc = "初始化预设作业，包含一个简单场景和一个车辆，用于用户初次试用体验。"
        job.status = "waiting"
        job.user_id = user.id
        job.company_id = user.company_id
        job.car_id = 1
        job.render_mode = "render"
        job.controller = "Oasis Driver_感知规控版"
        job.controller_version = "1.0.0"
        job.scenario_ids = [1]
        await job.save()

        task = Tasks()
        task.name = "default_scenario01"
        task.desc = "scenario"
        task.user_id = user.id
        task.company_id = user.company_id
        task.job_id = job.id
        task.job_name = "渲染模式预置场景"
        task.scenario_id = 1
        task.scenario_tags = [1]
        task.status = "waiting"
        await task.save()

        job = Jobs()
        job.name = "线框模式预置场景"
        job.desc = "初始化预设作业，包含一个简单场景和一个车辆，用于用户初次试用体验。"
        job.status = "waiting"
        job.user_id = user.id
        job.company_id = user.company_id
        job.car_id = 2
        job.render_mode = "norender"
        job.controller = "Oasis Driver_规控版"
        job.controller_version = "1.0.0"
        job.scenario_ids = [2]
        await job.save()

        task = Tasks()
        task.name = "default_scenario02"
        task.desc = "scenario"
        task.user_id = user.id
        task.company_id = user.company_id
        task.job_id = job.id
        task.job_name = "线框模式预置场景"
        task.scenario_id = 2
        task.scenario_tags = [2]
        task.status = "waiting"
        await task.save()

        scenario_model = Scenarios()
        scenario_model.name = '自定义文件夹'
        scenario_model.parent_id = 0
        scenario_model.type = "dir"
        scenario_model.user_id = user.id
        scenario_model.company_id = user.company_id
        await scenario_model.save()
        ret_dict = {}
        file_name = "front_GoAlong_av:2_rp:20_rv:6"
        ret_dict[file_name] = {}
        ret_dict[file_name]["content_error"] = []
        ret_dict[file_name]['name_exist_error'] = ''
        ret_dict[file_name]['upload_result'] = ''
        scenario_dic = {"_partial": False, "_saved_in_db": True, "_custom_generated_pk": False, "invalid": 0,
                        "parent_id": 2942, "user_id": 13, "id": 2996, "desc": "", "company_id": 1, "map_name": "Town02",
                        "type": "file", "name": "front_GoAlong_av:2_rp:25_rv:6", "criterion_id": 0, "lever": None,
                        "system_data": False, "is_temp": False,
                        "open_scenario_json":
                        {"basic": {"xodr": "Town02", "traffic": "False", "description": "front_GoAlong_av:2_rp:25_rv:6"},
                        "init_entities":
                            [{"name": "ego_vehicle", "type": "vehicle",
                             "speed": {"type": "absolute", "params": {"value": "2", "continuous": "undefined"}},
                                "end_position": {
                                  "type": "worldposition",
                                  "params":
                                      {"h": "0", "p": "0", "r": "0", "s": "undefined",  "t": "undefined",
                                       "x": "169.041", "y": "-306.753", "z": "0", "ds": "undefined",
                                       "dt": "undefined", "dx": "undefined", "dy": "undefined", "dz": "undefined",
                                       "dlane": "undefined", "laneid": "undefined", "offset": "undefined",
                                       "orientation": {"h": "0", "p": "0", "r": "0"}}},
                                       "start_position": {"type": "laneposition",
                                       "params": {
                                           "h": "359.981", "p": "0", "r": "0", "s": "10", "t": "undefined",
                                           "x": "62.659", "y": "-306.445", "z": "0", "ds": "undefined",
                                           "dt": "undefined", "dx": "undefined", "dy": "undefined",
                                           "dz": "undefined", "dlane": "undefined", "laneid": "-1",
                                           "offset": "0.09", "roadid": "19", "orientation":
                                           {"h": "359.981", "p": "0", "r": "0", "reftype": "absolute"}}}},
                                           {"name": "vehicle_001", "type": "vehicle", "model": "vehicle.audi.a2",
                                           "speed": {"type": "absolute", "params": {"value": "6", "continuous": "undefined"}},
                                           "start_position": {
                                               "type": "laneposition",
                                               "params": {"h": "359.981", "p": "0", "r": "0", "s": "35", "t": "undefined",
                                                        "x": "undefined", "y": "undefined", "z": "undefined",
                                                        "ds": "undefined", "dt": "undefined", "dx": "undefined",
                                                        "dy": "undefined", "dz": "undefined", "dlane": "undefined",
                                                         "laneid": "-1", "offset": "-0.056", "roadid": "19",
                                                         "orientation": {"h": "359.981", "p": "0", "r": "0",
                                                                         "reftype": "absolute"}}}}],
                         "init_environment": {"weather":
                                             {"wetness": "0", "cloudiness": "10", "cloudstate": "free",
                                             "fog_density": "10", "fog_falloff": "1", "fog_distance": "75",
                                              "precipitation": "0", "sky_visibility": "True", "wind_intensity": "10",
                                              "fog_visualrange": "10000", "sun_azimuth_angle": "160",
                                              "sun_altitude_angle": "20", "precipitation_deposits": "0"}},
                         "triggers_actions": []},
                        "ui_entities_json": {"mainCar": {"id": 1673519394592, "name": "Ego",
                        "statusEvent": {"initStatus": {"end": {"h": 0, "p": 0, "r": 0, "x": 169.041, "y": -306.753,
                                        "z": 0, "type": "worldposition"}, "speed": {"type": "absolute", "value": 2},
                                        "start": {"h": 359.981, "p": 0, "r": 0, "s": 10, "x": 62.659, "y": -306.445,
                                                  "z": 0, "fx": 0, "fy": 0, "fz": 0, "type": "laneposition",
                                                  "laneid": -1, "offset": 0.09, "roadid": "19", "reftype": "absolute"}},
                                        "scenarioEvents": []}}, "players":
                            [{"id": 1673519403669, "name": "vehicle_001", "type": "vehicle", "model": "vehicle.audi.a2",
                              "subType": "passenger", "statusEvent":
                                  {"initStatus": {"speed": {"type": "absolute", "value": 6},
                                                  "start": {"h": 359.981, "p": 0, "r": 0, "s": 35, "fx": 0, "fy": 0,
                                                            "fz": 0, "type": "laneposition", "laneid": -1,
                                                            "offset": -0.056, "roadid": "19", "reftype": "absolute"}},
                                   "scenarioEvents": []}}]}, "traffic_flow": [],
                        "environment": {"light_param": {"sun_azimuth_angle": 160, "sun_altitude_angle": 20},
                                        "weather_param":
                                            {"wetness": 0, "cloudiness": 10, "cloudstate": "free",
                                             "fog_density": 10, "fog_falloff": 1, "fog_distance": 75,
                                             "precipitation": 0, "sky_visibility": True, "wind_intensity": 10,
                                             "fog_visualrange": 10000, "precipitation_deposits": 0}},
                        "modified_at": "2023-01-12 18:31:02", "evaluation_standard":
                            {"jerk": {"enabled": False, "JerkLateralTest": 15, "JerkLongitudinalTest": 5},
                             "velocity": {"enabled": True, "MaxVelocityTest": 120, "MinVelocityTest": 0},
                             "OnRoadTest": True, "templateId": "", "useTemplate": False,
                             "acceleration": {"enabled": True, "AccelerationLateralTest": 2.3,
                             "AccelerationVerticalTest": 0.15, "AccelerationLongitudinalTest": 6},
                             "CollisionTest": True, "RunRedLightTest": True,
                             "averageVelocity":
                                 {"enabled": False, "MaxAverageVelocityTest": 120, "MinAverageVelocityTest": 0},
                                  "OntoSolidLineTest": True, "DrivenDistanceTest": True,
                                  "RoadSpeedLimitTest": True, "ReachDestinationTest": True},
                                  "tags": [], "created_at": "2023-01-12 18:31:02"}
        scenario_dic['system_data'] = 0
        scenario_dic["user_id"] = user.id
        scenario_dic["company_id"] = user.company_id
        scenario_dic['parent_id'] = scenario_model.parent_id
        scenario_json = json.dumps(scenario_dic)
        await upload_scenario(0, scenario_json, "cartel", False, file_name, {}, ['自定义文件夹'], user)
        dynamic = await Dynamics.filter(name="model3", invalid=0).first()
        diy_car = {
            "name": "自定义车辆",
            "desc": "初始预置主车，参数使用默认参数，用户可自定义编辑。",
            "type": "vehicle.tesla.model3",
            "light_state": "LowBeam",
            "vehicle_color": "242, 234, 78",
            "dynamics_id": dynamic.id if dynamic else 1,
            "render_mode": "norender",
            "company_id": user.company_id,
            "user_id": user.id
        }
        car = Cars(**diy_car)
        await car.save()
        sensor = await Sensors.filter(name='Oasis 理想传感器', invalid=0).first()
        diy_car_sensor = {
                "name": "Oasis 理想传感器模型",
                "nick_name": "理想传感器",
                "car_id": car.id,
                "sensor_id": sensor.id if sensor else 15,
                "type": "sensor.lidar.goal",
                "position_x": 0.0,
                "position_y": 0.0,
                "position_z": 1.0,
                "roll": 0,
                "pitch": 0,
                "yaw": 0,
                "data_record": False,
                "company_id": user.company_id,
                "user_id": user.id
            }
        carsensor = CarSensors(**diy_car_sensor)
        await carsensor.save()
        not_in_list = ["Oasis 深度摄像头", "Oasis 鱼眼摄像头", "RS-LiDAR-M1", "AT128", "Pandar64",
                       "Oasis 目标级激光雷达", "Oasis 理想传感器", "Oasis APA"]
        for sensor in cam_list:
            if sensor['name'] in not_in_list:
                continue
            if sensor['name'] == "Oasis RGB摄像头":
                sensor['name'] = "自定义摄像头"
                sensor['desc'] = '初始预置摄像头模型，参数使用默认参数，用户可自定义编辑。'
            elif sensor['name'] == 'Oasis 目标级摄像头':
                sensor['name'] = '自定义目标传感器'
                sensor['desc'] = '初始预置目标级传感器，参数使用默认参数，用户可自定义编辑。'
            elif sensor['name'] == 'Oasis 激光雷达':
                sensor['name'] = '自定义激光雷达'
                sensor['desc'] = '初始预置激光雷达，参数使用默认参数，用户可自定义编辑。'
            elif sensor['name'] == 'Oasis 毫米波雷达':
                sensor['name'] = '自定义毫米波雷达'
                sensor['desc'] = '初始预置毫米波雷达，参数使用默认参数，用户可自定义编辑。'
            elif sensor['name'] == 'Oasis UPA':
                sensor['name'] = '自定义超声波雷达'
                sensor['desc'] = '初始预置超声波雷达，参数使用默认参数，用户可自定义编辑。'
            elif sensor['name'] == 'Oasis GNSS':
                sensor['name'] = '自定义GNSS'
                sensor['desc'] = '初始预置GNSS传感器，参数使用默认参数，用户可自定义编辑。'
            elif sensor['name'] == 'Oasis IMU':
                sensor['name'] = '自定义IMU'
                sensor['desc'] = '初始预置IMU传感器，参数使用默认参数，用户可自定义编辑。'
            sensor['user_id'] = user.id
            sensor['company_id'] = user.company_id
            sen = Sensors(**sensor)
            await sen.save()