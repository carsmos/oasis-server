import shortuuid

from sdgApp.Application.weather.usercase import WeatherQueryUsercase
from sdgApp.Application.log.usercase import except_logger


@except_logger("insert_defaultfailed............")
async def insert_default(db_session, user):
    from sdgApp.Application.sensor.usercase import SensorCommandUsercase, SensorQueryUsercase
    from sdgApp.Application.sensor.CommandDTOs import SensorCreateDTO

    depth_cam = {
        "name": "基础深度相机模型",
        "type": "sensor.camera.depth",
        "desc": "初始化深度相机模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。",
        "param": {
            "id": "front",
            "roll": 0,
            "pitch": 0,
            "yaw": 0,
            "fov": 90,
            "image_size_x": 400,
            "image_size_y": 70,
            "sensor_tick": 0.05,
            "lens_circle_falloff": 5,
            "lens_circle_multiplier": 0,
            "lens_k": -1,
            "lens_kcube": 0,
            "lens_x_size": 0.08,
            "lens_y_size": 0.08
        }
    }
    rgb_cam = {
        "name": "基础RGB摄像机模型",
        "type": "sensor.camera.rgb",
        "desc": "初始化RGB摄像机模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。",
        "param": {
            "id": "front",
            "roll": 0,
            "pitch": 0,
            "yaw": 0,
            "bloom_intensity": 0.675,
            "fov": 90,
            "fstop": 1.4,
            "image_size_x": 800,
            "image_size_y": 600,
            "iso": 100,
            "gamma": 2.2,
            "lens_flare_intensity": 0.1,
            "sensor_tick": 0.05,
            "shutter_speed": 200,
            "lens_circle_falloff": 5,
            "lens_circle_multiplier": 0,
            "lens_k": -1,
            "lens_kcube": 0,
            "lens_x_size": 0.08,
            "lens_y_size": 0.08,
            "min_fstop": 1.2,
            "blade_count": 5,
            "exposure_mode": "histogram",
            "exposure_compensation": 0,
            "exposure_min_bright": 10,
            "exposure_max_bright": 12,
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
            "enable_postprocess_effects": True
        }
    }
    sematic_cam = {
        "name": "基础语义分割摄像机模型",
        "type": "sensor.camera.semantic_segmentation",
        "desc": "初始化语义分割摄像机模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。",
        "param": {
            "id": "front",
            "roll": 0,
            "pitch": 0,
            "yaw": 0,
            "fov": 90,
            "image_size_x": 800,
            "image_size_y": 600,
            "sensor_tick": 0.05,
            "lens_circle_falloff": 5,
            "lens_circle_multiplier": 0,
            "lens_k": -1,
            "lens_kcube": 0,
            "lens_x_size": 0.08,
            "lens_y_size": 0.08
        }
    }

    dvs_cam = {
        "name": "基础DVS摄像机模型",
        "type": "sensor.camera.dvs",
        "desc": "初始化DVS摄像机模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。",
        "param": {
            "id": "front",
            "roll": 0,
            "pitch": 0,
            "yaw": 0,
            "bloom_intensity": 0.675,
            "fov": 90,
            "fstop": 1.4,
            "image_size_x": 800,
            "image_size_y": 600,
            "iso": 100,
            "gamma": 2.2,
            "lens_flare_intensity": 0.1,
            "sensor_tick": 0.05,
            "shutter_speed": 200,
            "positive_threshold": 0.3,
            "negative_threshold": 0.3,
            "sigma_positive_threshold": 0,
            "sigma_negative_threshold": 0,
            "use_log": True,
            "log_eps": 0.001,
            "lens_circle_falloff": 5,
            "lens_circle_multiplier": 0,
            "lens_k": -1,
            "lens_kcube": 0,
            "lens_x_size": 0.08,
            "lens_y_size": 0.08,
            "min_fstop": 1.2,
            "blade_count": 5,
            "exposure_mode": "histogram",
            "exposure_compensation": 0,
            "exposure_min_bright": 10,
            "exposure_max_bright": 12,
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
            "enable_postprocess_effects": True
        }
    }
    collision_detector = {
        "name": "基础碰撞检测器模型",
        "type": "sensor.other.collision",
        "desc": "初始化碰撞检测器模型，可用于用户初次使用系统体验使用。",
        "param": {
            "id": "front"
        }
    }
    lane_detector = {
        "name": "基础车道入侵检测器模型",
        "type": "sensor.other.lane_invasion",
        "desc": "初始化车道入侵检测器模型，可用于用户初次使用系统体验使用。\n",
        "param": {
            "id": "front"
        }
    }

    obstacle_detector = {
        "name": "基础障碍物检测器模型",
        "type": "sensor.other.obstacle",
        "desc": "初始化障碍物检测器模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。",
        "param": {
            "id": "front",
            "distance": 5,
            "hit_radius": 0.5,
            "only_dynamics": False,
            "debug_linetrace": False,
            "sensor_tick": 0
        }
    }

    gnss = {
        "name": "基础导航卫星传感器模型",
        "type": "sensor.other.gnss",
        "desc": "初始化导航卫星传感器模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。",
        "param": {
            "id": "front",
            "noise_alt_bias": 0,
            "noise_alt_stddev": 0,
            "noise_lat_bias": 0,
            "noise_lat_stddev": 0,
            "noise_lon_bias": 0,
            "noise_lon_stddev": 0,
            "noise_seed": 0,
            "sensor_tick": 0
        }
    }

    imu = {
        "name": "基础IMU传感器模型",
        "type": "sensor.other.imu",
        "desc": "初始化IMU传感器模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。",
        "param": {
            "id": "front",
            "roll": 0,
            "pitch": 0,
            "yaw": 0,
            "noise_accel_stddev_x": 0,
            "noise_accel_stddev_y": 0,
            "noise_accel_stddev_z": 0,
            "noise_gyro_stddev_x": 0,
            "noise_gyro_stddev_y": 0,
            "noise_gyro_stddev_z": 0,
            "noise_gyro_bias_x": 0,
            "noise_gyro_bias_y": 0,
            "noise_gyro_bias_z": 0,
            "noise_seed": 0,
            "sensor_tick": 0
        }
    }

    lidar = {
        "name": "基础激光雷达传感器模型",
        "type": "sensor.lidar.ray_cast",
        "desc": "初始化激光雷达传感器模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。",
        "param": {
            "id": "front",
            "roll": 0,
            "pitch": 0,
            "yaw": 0,
            "range": 10,
            "channels": 32,
            "points_per_second": 320000,
            "rotation_frequency": 20,
            "upper_fov": 10,
            "lower_fov": -30,
            "atmosphere_attenuation_rate": 0.004,
            "dropoff_general_rate": 0.45,
            "dropoff_intensity_limit": 0.8,
            "dropoff_zero_intensity": 0.4,
            "sensor_tick": 0.05,
            "noise_stddev": 0
        }
    }

    ray_semantic = {
        "name": "基础语义激光雷达传感器模型",
        "type": "sensor.lidar.ray_cast_semantic",
        "desc": "初始化语义激光雷达传感器模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。\n",
        "param": {
            "id": "front",
            "roll": 0,
            "pitch": 0,
            "yaw": 0,
            "range": 10,
            "channels": 32,
            "points_per_second": 320000,
            "rotation_frequency": 20,
            "upper_fov": 10,
            "lower_fov": -30,
            "sensor_tick": 0.05
        }
    }

    radar = {
        "name": "基础雷达传感器模型",
        "type": "sensor.other.radar",
        "desc": "初始化雷达传感器模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。",
        "param": {
            "id": "front",
            "roll": 0,
            "pitch": 0,
            "yaw": 0,
            "range": 100,
            "vertical_fov": 10,
            "points_per_second": 1500,
            "sensor_tick": 0
        }
    }

    rss = {
        "name": "基础RSS传感器模型",
        "type": "sensor.other.rss",
        "desc": "初始化RSS传感器模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。",
        "param": {
            "id": "front",
            "roll": 0,
            "pitch": 0,
            "yaw": 0
        }
    }

    await SensorCommandUsercase(db_session=db_session, user=user).create_sensor(SensorCreateDTO(**lidar))
    lidar_dto = await SensorQueryUsercase(db_session=db_session, user=user).list_sensor(1, 15, {})
    lidar_dto = lidar_dto["datas"][0]

    await SensorCommandUsercase(db_session=db_session, user=user).create_sensor(SensorCreateDTO(**depth_cam))
    depth_dto = await SensorQueryUsercase(db_session=db_session, user=user).list_sensor(1, 15, {})
    depth_dto = depth_dto["datas"][1]

    other_default_sensors = [rss,
                             radar,
                             ray_semantic,
                             imu,
                             gnss,
                             obstacle_detector,
                             lane_detector,
                             collision_detector,
                             dvs_cam,
                             sematic_cam,
                             rgb_cam]

    for default_sensor in other_default_sensors:
        await SensorCommandUsercase(db_session=db_session, user=user).create_sensor(SensorCreateDTO(**default_sensor))

    sensor_dic = await SensorQueryUsercase(db_session=db_session, user=user).list_sensor(1, 15, {})
    sensor_list = sensor_dic['datas']
    rgb_cam = [sensor for sensor in sensor_list if "RGB" in sensor.name][0]
    dvs_cam = [sensor for sensor in sensor_list if "DVS" in sensor.name][0]

    from sdgApp.Application.dynamics.usercase import DynamicsCommandUsercase, DynamicsQueryUsercase
    from sdgApp.Application.dynamics.CommandDTOs import DynamicsCreateDTO

    default_dynamic = {
        "name": "基础动力学模型",
        "desc": "初始化动力学模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。",
        "param": {
            "torque_curve": [
                {
                    "x": "0",
                    "y": "400"
                },
                {
                    "x": "600",
                    "y": "1300"
                }
            ],
            "steering_curve": [
                {
                    "x": "0",
                    "y": "1"
                },
                {
                    "x": "1",
                    "y": "100"
                },
                {
                    "x": "3",
                    "y": "300"
                }
            ],
            "max_rpm": 10000,
            "moi": 1,
            "damping_rate_full_throttle": 0,
            "use_gear_autobox": False,
            "gear_switch_time": 0.5,
            "clutch_strength": 10,
            "mass": 10000,
            "center_of_mass": "0.0,0.0,0.0",
            "drag_coefficient": 0.25,
            "use_sweep_wheel_collision": True,
            "final_ratio": 4,
            "damping_rate_zero_throttle_clutch_engaged": 2,
            "damping_rate_zero_throttle_clutch_disengaged": 0.35,
            "wheels": {
                "front_left_wheel": {
                    "position": {"x": 0, "y": 0, "z": 0},
                    "tire_friction": "2.0",
                    "damping_rate": "0.25",
                    "max_steer_angle": "70.0",
                    "radius": "30.0",
                    "max_brake_torque": "1500.0",
                    "max_handbrake_torque": "3000.0",
                    "long_stiff_value": "",
                    "lat_stiff_max_load": "",
                    "lat_stiff_value": ""
                },
                "front_right_wheel": {
                    "position": {"x": 0, "y": 0, "z": 0},
                    "tire_friction": "2.0",
                    "damping_rate": "0.25",
                    "max_steer_angle": "70.0",
                    "radius": "30.0",
                    "max_brake_torque": "1500.0",
                    "max_handbrake_torque": "3000.0",
                    "long_stiff_value": "",
                    "lat_stiff_max_load": "",
                    "lat_stiff_value": ""
                },
                "rear_left_wheel": {
                    "position": {"x": 0, "y": 0, "z": 0},
                    "tire_friction": "2.0",
                    "damping_rate": "0.25",
                    "max_steer_angle": "70.0",
                    "radius": "30.0",
                    "max_brake_torque": "1500.0",
                    "max_handbrake_torque": "3000.0",
                    "long_stiff_value": "",
                    "lat_stiff_max_load": "",
                    "lat_stiff_value": ""
                },
                "rear_right_wheel": {
                    "position": {"x": 0, "y": 0, "z": 0},
                    "tire_friction": "2.0",
                    "damping_rate": "0.25",
                    "max_steer_angle": "70.0",
                    "radius": "30.0",
                    "max_brake_torque": "1500.0",
                    "max_handbrake_torque": "3000.0",
                    "long_stiff_value": "",
                    "lat_stiff_max_load": "",
                    "lat_stiff_value": ""
                }
            }
        }
    }

    await DynamicsCommandUsercase(db_session=db_session, user=user).create_dynamics(
        DynamicsCreateDTO(**default_dynamic))
    dynamic_dto = await DynamicsQueryUsercase(db_session=db_session, user=user).list_dynamics(0, 15, "")
    dynamic_dto = dynamic_dto["datas"][0]

    from sdgApp.Application.CarFacadeService.AssembleService import AssembleCarService
    from sdgApp.Application.CarFacadeService.CommandDTOs import AssembleCreateDTO
    from sdgApp.Application.car.usercase import CarQueryUsercase

    assemble_car_dict = {
        "name": "基础车辆",
        "desc": "初始化预设车辆，所有配置使用简单匹配置，用于用户初次使用系统试用。",
        "param": {
            "type": "vehicle.tesla.model3",
            "light_state": "LowBeam",
            "vehicle_color": "242, 234, 78",
            "controller": "autoware"
        },
        "dynamics_id": dynamic_dto.id,
        "sensors": [
            {"id": lidar_dto.id, "position": {"x": "0.0", "y": "0.0", "z": "2.4"}},
            {"id": depth_dto.id, "position": {"x": "2.0", "y": "0.0", "z": "2.0"}},
            {"id": rgb_cam.id, "position": {"x": "1.0", "y": "0.0", "z": "3.0"}},
            {"id": dvs_cam.id, "position": {"x": "3.0", "y": "0.0", "z": "4.0"}}
        ]}
    await AssembleCarService(AssembleCreateDTO(**assemble_car_dict), db_session=db_session, user=user)
    default_car_dto = await CarQueryUsercase(db_session=db_session, user=user).list_car(1, 15, None)
    default_car_dto = default_car_dto["datas"][0]

    from sdgApp.Application.weather.usercase import WeatherCommandUsercase
    from sdgApp.Application.weather.CommandDTOs import WeatherCreateDTO

    default_weather_1 = {
        "name": "Clear",
        "desc": "初始化场景天气模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。\n",
        "param": {
            "cloudiness": 15.0,
            "precipitation": 0.0,
            "precipitation_deposits": 0.0,
            "wind_intensity": 0.35,
            "fog_density": 0.0,
            "fog_distance": 0.0,
            "wetness": 0.0,
            "fog_falloff": 0.0,
        }
    }

    default_weather_2 = {
        "name": "Cloudy",
        "desc": "初始化场景天气模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。\n",
        "param": {
            "cloudiness": 80.0,
            "precipitation": 0.0,
            "precipitation_deposits": 0.0,
            "wind_intensity": 0.35,
            "fog_density": 0.0,
            "fog_distance": 0.0,
            "wetness": 0.0,
            "fog_falloff": 0.0,
        }
    }

    default_weather_3 = {
        "name": "HardRain",
        "desc": "初始化场景天气模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。\n",
        "param": {
            "cloudiness": 90.0,
            "precipitation": 60.0,
            "precipitation_deposits": 100.0,
            "wind_intensity": 1.0,
            "fog_density": 0.0,
            "fog_distance": 0.0,
            "wetness": 0.0,
            "fog_falloff": 0.0,
        }
    }

    default_weather_4 = {
        "name": "MidRain",
        "desc": "初始化场景天气模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。\n",
        "param": {
            "cloudiness": 80.0,
            "precipitation": 30.0,
            "precipitation_deposits": 50.0,
            "wind_intensity": 0.4,
            "fog_density": 0.0,
            "fog_distance": 0.0,
            "wetness": 0.0,
            "fog_falloff": 0.0,
        }
    }

    default_weather_5 = {
        "name": "SoftRain",
        "desc": "初始化场景天气模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。\n",
        "param": {
            "cloudiness": 70.0,
            "precipitation": 15.0,
            "precipitation_deposits": 50.0,
            "wind_intensity": 0.35,
            "fog_density": 0.0,
            "fog_distance": 0.0,
            "wetness": 0.0,
            "fog_falloff": 0.0,
        }
    }

    default_weather_6 = {
        "name": "WetCloudy",
        "desc": "初始化场景天气模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。\n",
        "param": {
            "cloudiness": 80.0,
            "precipitation": 0.0,
            "precipitation_deposits": 50.0,
            "wind_intensity": 0.35,
            "fog_density": 0.0,
            "fog_distance": 0.0,
            "wetness": 0.0,
            "fog_falloff": 0.0,
        }
    }

    default_weather_7 = {
        "name": "Wet",
        "desc": "初始化场景天气模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。\n",
        "param": {
            "cloudiness": 20.0,
            "precipitation": 0.0,
            "precipitation_deposits": 50.0,
            "wind_intensity": 0.35,
            "fog_density": 0.0,
            "fog_distance": 0.0,
            "wetness": 0.0,
            "fog_falloff": 0.0,
        }
    }
    for weather in [default_weather_1, default_weather_2, default_weather_3, default_weather_4, default_weather_5,
                    default_weather_6, default_weather_7]:
        await WeatherCommandUsercase(db_session=db_session, user=user).create_weather(WeatherCreateDTO(**weather))

    from sdgApp.Application.light.usercase import LightCommandUsercase
    from sdgApp.Application.light.CommandDTOs import LightCreateDTO

    default_light_1 = {
        "name": "清晨",
        "desc": "初始化光照模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。\n",
        "param": {
            "sun_altitude_angle": 45.0,
            "sun_azimuth_angle": 90.0,
        }
    }
    default_light_2 = {
        "name": "上午",
        "desc": "初始化光照模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。\n",
        "param": {
            "sun_altitude_angle": 75.0,
            "sun_azimuth_angle": 135.0,
        }
    }
    default_light_3 = {
        "name": "正午",
        "desc": "初始化光照模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。\n",
        "param": {
            "sun_altitude_angle": 90.0,
            "sun_azimuth_angle": 180.0,
        }
    }
    default_light_4 = {
        "name": "午后",
        "desc": "初始化光照模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。\n",
        "param": {
            "sun_altitude_angle": 45.0,
            "sun_azimuth_angle": 225.0,
        }
    }
    default_light_5 = {
        "name": "黄昏",
        "desc": "初始化光照模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。\n",
        "param": {
            "sun_altitude_angle": 15.0,
            "sun_azimuth_angle": 270.0,
        }
    }
    default_light_6 = {
        "name": "午夜",
        "desc": "初始化光照模型，所有参数均使用默认配置，可用于用户初次使用系统体验使用。\n",
        "param": {
            "sun_altitude_angle": -90.0,
            "sun_azimuth_angle": 360.0,
        }
    }
    for light in [default_light_1, default_light_2, default_light_3, default_light_4, default_light_5, default_light_6]:
        await LightCommandUsercase(db_session=db_session, user=user).create_light(LightCreateDTO(**light))

    from sdgApp.Application.dynamic_scenes.usercase import DynamicSceneCommandUsercase, DynamicSceneQueryUsercase
    from sdgApp.Application.dynamic_scenes.CommandDTOs import DynamicSceneCreateDTO

    default_scene_1 = {
        "name": "动态场景描述1",
        "desc": "推荐使用地图 Town3",
        "scene_script": "// ego car\nego_init_position = (30,134); //default coordinate frame is ENU\nego_target_position = (140,134); //default coordinate frame is ENU\nego_init_state = (ego_init_position);\nego_target_state = (ego_target_position);\nego_vehicle = AV(ego_init_state, ego_target_state, vehicle_type);\n\n//npc1\nnpc_init_state = ((55,134),,2.7); // start\nnpc_target_state = ((120,134),,0.0); // target\nnpc1= Vehicle(npc_init_state,, npc_target_state);\n\nnpcs = {npc1};\n\n// pedestrian\npedestrian_type = (1.65, black);\npedestrian1 = Pedestrian(((-15.9, 110), ,0.5), , ((-56, 123), ,0), pedestrian_type);\npedestrian2 = Pedestrian(((101, 62), ,0.5), , ((120, 144), ,0), pedestrian_type);\npedestrians={pedestrian1, pedestrian2};\n\n\n//traffic requirements\nspeed_range = (0,20);\nspeed_limit = SpeedLimit(\"52.-1\", speed_range);\nintersection = Intersection(1, 1, 0, 1);\ntraffic = {intersection,speed_limit};\n\nscenario = CreateScenario{load(map);\n\t\t\t        ego_vehicle;\n\t\t\t        npcs;\n\t\t\t        {};\n\t\t\t        {};\n\t\t\t        env;\n\t\t\t        traffic;\n};",
        "type": "scenest"
    }

    await DynamicSceneCommandUsercase(db_session=db_session, user=user).create_scenario(
        DynamicSceneCreateDTO(**default_scene_1))
    default_scene_dto = await DynamicSceneQueryUsercase(db_session=db_session, user=user).find_all_scenarios(1, 15, "")
    default_scene_dto = default_scene_dto["datas"][0]

    scene_2 = {
        "name": "动态场景描述2",
        "desc": "推荐使用地图 Town3",
        "scene_script": "// ego car\nego_init_position = (-110,3); //default coordinate frame is ENU\nego_target_position = (170,-60); //default coordinate frame is ENU\nego_init_state = (ego_init_position);\nego_target_state = (ego_target_position);\nego_vehicle = AV(ego_init_state, ego_target_state, vehicle_type);\n\n// npcs\nnpc1=Vehicle(((-3,-45),,-1),,((245.3,-75)));\nnpc2=Vehicle(((-3,-52),,-1),, ((245.3,-60)));\nnpc3=Vehicle(((-85,-40),,-1),, ((234.8,120)));\nnpc4=Vehicle(((-85,-50),,-1),, ((234.8,50)));\nnpc5=Vehicle(((-88.5,-43),,-1),,((234.8,150)));\nnpc6=Vehicle(((-77,30),,-1),,((140,-1)));\nnpc7=Vehicle(((-77,-37),,-1),,((170,-4.5)));\nnpc8=Vehicle(((23,23),,-1),,((170,-4.5)));\nnpc9=Vehicle(((-67,230),,-1),,((170,-4.5)));\nnpc10=Vehicle(((89,77),,-1),,((170,-4.5)));\nnpc11=Vehicle(((-250,199),,-1),,((170,-4.5)));\nnpc12=Vehicle(((-63,0),,-1),,((170,-4.5)));\nnpc13=Vehicle(((-55,0),,-1),,((170,-4.5)));\nnpc14=Vehicle(((-45,1),,-1),,((170,-4.5)));\nnpc15=Vehicle(((-35,3),,-1),,((170,-4.5)));\nnpc16=Vehicle(((-25,3),,-1),,((170,-4.5)));\nnpc17=Vehicle(((-15,3),,-1),,((170,-4.5)));\nnpc18=Vehicle(((-5,3),,-1),,((170,-4.5)));\nnpc19=Vehicle(((5,3),,-1),,((170,-4.5)));\nnpc20=Vehicle(((-77,-45),,-1),,((170,-4.5)));\nnpc21=Vehicle(((-20,-6),,-1),,((170,-4.5)));\nnpc22=Vehicle(((-88,-5),,-1),,((170,-4.5)));\nnpc23=Vehicle(((20,3),,-1),,((170,-4.5)));\nnpc24=Vehicle(((40,3),,-1),,((170,-4.5)));\nnpc25=Vehicle(((65,0),,-1),,((170,-4.5)));\nnpc26=Vehicle(((45,-3),,-1),,((170,-4.5)));\nnpc27=Vehicle(((30,-3),,-1),,((170,-4.5)));\nnpc28=Vehicle(((15,-3),,-1),,((170,-4.5)));\nnpc29=Vehicle(((5,-3),,-1),,((170,-4.5)));\nnpc30=Vehicle(((-5,-3),,-1),,((170,-4.5)));\nnpc31=Vehicle(((-15,-3),,-1),,((170,-4.5)));\nnpc32=Vehicle(((-25,-3),,-1),,((170,-4.5)));\nnpc33=Vehicle(((5,35),,-1),,((170,-4.5)));\nnpc34=Vehicle(((-80,1),,-1),,((170,-4.5)));\nnpc35=Vehicle(((-85,1),,-1),,((170,-4.5)));\nnpc36=Vehicle(((-63,-3),,-1),,((170,-4.5)));\nnpc37=Vehicle(((45,-3),,-1),,((170,-4.5)));\nnpc38=Vehicle(((55,-3),,-1),,((170,-4.5)));\nnpc39=Vehicle(((65,-6),,-1),,((170,-4.5)));\nnpc40=Vehicle(((75,-6),,-1),,((170,-4.5)));\nnpc41=Vehicle(((3,63),,-1),,((170,-4.5)));\nnpc42=Vehicle(((-3,53),,-1),,((170,-4.5)));\nnpc43=Vehicle(((3,43),,-1),,((170,-4.5)));\nnpc44=Vehicle(((6,33),,-1),,((170,-4.5)));\nnpc45=Vehicle(((-3,23),,-1),,((170,-4.5)));\nnpc46=Vehicle(((6,13),,-1),,((170,-4.5)));\nnpc47=Vehicle(((3,3),,-1),,((170,-4.5)));\nnpc48=Vehicle(((3,-5),,-1),,((170,-4.5)));\nnpc49=Vehicle(((6,-15),,-1),,((170,-4.5)));\nnpc50=Vehicle(((3,-25),,-1),,((170,-4.5)));\nnpc51=Vehicle(((-3,63),,-1),,((170,-4.5)));\nnpc52=Vehicle(((-5,53),,-1),,((170,-4.5)));\nnpc53=Vehicle(((-3,43),,-1),,((170,-4.5)));\nnpc54=Vehicle(((-5,33),,-1),,((170,-4.5)));\nnpc55=Vehicle(((-3,23),,-1),,((170,-4.5)));\nnpc56=Vehicle(((-5,13),,-1),,((170,-4.5)));\nnpc57=Vehicle(((5,23),,-1),,((170,-4.5)));\nnpc58=Vehicle(((-3,-6),,-1),,((170,-4.5)));\nnpc59=Vehicle(((-3,-16),,-1),,((170,-4.5)));\nnpc60=Vehicle(((-3,-32),,-1),,((-170,-4.5)));\n\nnpcs = {npc1,npc2,npc3,npc4,npc5,npc6,npc7,npc8,npc9,npc10,npc11,npc12};\n\n// pedestrian\npedestrian_type = (1.65, black);\npedestrian1 = Pedestrian(((-15.9, 110), ,0.5), , ((-56, 123), ,0), pedestrian_type);\npedestrian2 = Pedestrian(((101, 62), ,0.5), , ((120, 144), ,0), pedestrian_type);\npedestrians = {pedestrian1, pedestrian2};\n\n//traffic requirements\nspeed_range = (0,80);\nspeed_limit = SpeedLimit(\"10.-1\", speed_range);\nintersection = Intersection(1, 1, 0, 1);\ntraffic = {intersection, speed_limit};\n\nscenario = CreateScenario{load(map);\n        ego_vehicle;\n        npcs;\n        {};\n        {};\n        env;\n        traffic;\n};",
        "type": "scenest"
    }
    scene_3 = {
        "name": "动态场景描述3",
        "desc": "推荐使用地图 Town3",
        "scene_script": "scenario dut.cut_in_and_slow:\n  set_map(\"Town03\")   # specify map to use in this test\n path: Path                      # A path in the map\n path_min_driving_lanes(2)         # Path should have at least two lanes\n\n  ego_vehicle: Model3                # ego car\n  npc: Rubicon               # The other car\n\n  do serial:\n  get_ahead: parallel(duration: 30s):\n  ego_vehicle.drive(path) with:\n  speed(20kph)\n npc.drive(path) with:\n lane(right_of: ego_vehicle, at: start)\n position(15m, behind: ego_vehicle, at: start)\n position(20m, ahead_of: ego_vehicle, at: noend)\n\n change_lane: parallel(duration: 5s):\n ego_vehicle.drive(path)\n npc.drive(path) with:\n lane(same_as: ego_vehicle, at: noend)\n\n slow: parallel(duration: 20s):\n ego_vehicle.drive(path)\n npc.drive(path) with:\n speed(10kph)",
        "type": "cartel"
    }
    scene_4 = {
        "name": "动态场景描述4",
        "desc": "推荐使用地图 Town3",
        "scene_script": "// ego car\nego_init_position = (-35.84, -210.66); //default coordinate frame is ENU\nego_target_position = (-43.49, -209.36); //default coordinate frame is ENU\nego_init_state = (ego_init_position,,1);\nego_target_state = (ego_target_position,,1);\n\nego_vehicle = AV(ego_init_state, ego_target_state, vehicle_type);\n\n// npc car\nnpc1_init_state = ((151.03, -4.47),,5); // start\nnpc1_waypoint = ((3.5, -30));\nnpc1_target_state = ((4.2, -101),,5); 	// target\nnpc1_waypoints = (npc1_waypoint);\nnpc1 = Vehicle(npc1_init_state, Waypoint(npc1_waypoints), npc1_target_state);\n\n// npc car\nnpc2_init_state = ((137, -8.18),,5); 		// start\nnpc2_waypoint = ((83.42, -34.67));\nnpc2_target_state = ((42.88, -139.06),,5); // target\nnpc2_waypoints = (npc2_waypoint);\nnpc2 = Vehicle(npc2_init_state, Waypoint(npc2_waypoints), npc2_target_state);\n\nnpcs = {npc1, npc2};\n\n// pedestrian\npedestrian_type = (1.65, black);\npedestrian1 = Pedestrian(((-15.9, 110), ,0.5), , ((-56, 123), ,0), pedestrian_type);\npedestrian2 = Pedestrian(((101, 62), ,0.5), , ((120, 144), ,0), pedestrian_type);\npedestrians = {pedestrian1, pedestrian2};\n\n// traffic requirements\nspeed_range = (0, 20);\nspeed_limit = SpeedLimit(\"52.-1\", speed_range);\nintersection = Intersection(1, 1, 0, 1);\ntraffic = {intersection, speed_limit};\n\nscenario = CreateScenario{load(map);ego_vehicle;npcs;pedestrians;{};env;traffic;};",
        "type": "scenest"
    }
    scene_5 = {
        "name": "动态场景描述5",
        "desc": "推荐使用地图 Town3",
        "scene_script": "// ego car\nego_init_position = (101, 62.48); //default coordinate frame is ENU\nego_target_position = (165, 62.48); //default coordinate frame is ENU\nego_init_state = (ego_init_position);\nego_target_state = (ego_target_position);\n\nego_vehicle = AV(ego_init_state, ego_target_state, vehicle_type);\n\n// npc car\nnpc1_init_state = (\"52.-1\"->0.0, ,0.0); // start\nnpc1_waypoint = ((8,40));\nnpc1_target_state = (\"52.1\"->0.0, ,0.0); // target\nnpc1_waypoints = (npc1_waypoint);\nnpc1 = Vehicle(npc1_init_state, Waypoint(npc1_waypoints), npc1_target_state);\n\n// npc 2: move along given waypoints\nnpc2_init_state = (\"52.-1\"->5.0, ,0.0);		// start\nnpc2_waypoints = ((\"52.-1\"->5.0, ,0.0), (\"52.1\"->2.0, ,1.0));\nnpc2_target_state = (\"52.1\"->2.0, ,0.0); 	// target\nnpc2 = Vehicle(npc2_init_state, Waypoint(npc2_waypoints), npc2_target_state, \nvehicle_type);\n\n// npc 3: static vehicle\nnpc3 = Vehicle((\"75.-1\"->0.0, ,0.0), , (\"494.-1\"->1.0, ,0.0));\n\nnpcs = {npc1, npc2, npc3};\n\n// pedestrian\npedestrian_type = (1.65, black);\npedestrian1 = Pedestrian(((-15.9, 110), ,0.5), , ((-56, 123), ,0), pedestrian_type);\npedestrian2 = Pedestrian(((101, 62), ,0.5), , ((120, 144), ,0), pedestrian_type);\npedestrians = {pedestrian1, pedestrian2};\n\n// traffic requirements\nspeed_range = (0, 20);\nspeed_limit = SpeedLimit(\"52.-1\", speed_range);\nintersection = Intersection(1, 1, 0, 1);\ntraffic = {intersection, speed_limit};\n\nscenario = CreateScenario{load(map);ego_vehicle;npcs;pedestrians;{};env;traffic;};\n\nTrace trace = EXE(scenario);\n\nego_state= trace[1][ego];\nnpc2_perception= trace[1][perception][npc2];\nnpc2_state= trace[1][truth][npc2];\npedestrian_truth = trace[1][perception][pedestrian1];\npedestrian_ground = trace[1][truth][pedestrian1];\n\ndistance = dis(ego_state, npc2_state);\nerror = diff(npc2_perception, npc2_state);\nperception_detection = distance <= 3 & error <= 4;\ntrace |=G perception_detection;\nintersection_assertion=(trace[1][perception][traffic]==trace[1][truth][traffic]\n&trace[1][traffic]==red)->(~norm((100,100))U(trace[1][perception]\n[traffic]==trace[1][truth][traffic]\n&trace[1][traffic]==green));\ntrace |=G intersection_assertion;\nspeed_constraint_assertion=(trace[1][perception][traffic]==trace[1][truth][traffic]\n&trace[1][traffic]==(100,200)&120<trace[1][traffic][0])\n->F[0,2]~120<trace[1][traffic][0];\ntrace |=G speed_constraint_assertion;",
        "type": "scenest"
    }
    scene_6_openscenario = {
        "name": "动态场景描述6",
        "desc": "推荐使用地图 Town3",
        "scene_script": "<?xml version=\"1.0\"?>\n    <OpenSCENARIO>\n      <FileHeader revMajor=\"1\" revMinor=\"0\" date=\"2019-06-25T00:00:00\" description=\"CARLA:FollowLeadingVehicle\" author=\"\"/>\n      <ParameterDeclarations>\n        <ParameterDeclaration name=\"leadingSpeed\" parameterType=\"double\" value=\"2.0\"/>\n      </ParameterDeclarations>\n      <CatalogLocations>\n      </CatalogLocations>\n      <RoadNetwork>\n        <LogicFile filepath=\"Town03\"/>\n        <SceneGraphFile filepath=\"\"/>\n      </RoadNetwork>\n      <Entities>\n        <ScenarioObject name=\"ego_vehicle\">\n          <Vehicle name=\"vehicle.lincoln.mkz2017\" vehicleCategory=\"car\">\n            <ParameterDeclarations/>\n            <Performance maxSpeed=\"69.444\" maxAcceleration=\"10.0\" maxDeceleration=\"10.0\"/>\n            <BoundingBox>\n              <Center x=\"1.5\" y=\"0.0\" z=\"0.9\"/>\n              <Dimensions width=\"2.1\" length=\"4.5\" height=\"1.8\"/>\n            </BoundingBox>\n            <Axles>\n              <FrontAxle maxSteering=\"0.5\" wheelDiameter=\"0.6\" trackWidth=\"1.8\" positionX=\"3.1\" positionZ=\"0.3\"/>\n              <RearAxle maxSteering=\"0.0\" wheelDiameter=\"0.6\" trackWidth=\"1.8\" positionX=\"0.0\" positionZ=\"0.3\"/>\n            </Axles>\n            <Properties>\n              <Property name=\"type\" value=\"ego_vehicle\"/>\n              <Property name=\"color\" value=\"0,0,255\"/>\n            </Properties>\n          </Vehicle>\n        </ScenarioObject>\n        <ScenarioObject name=\"adversary\">\n          <Vehicle name=\"vehicle.lincoln.mkz2017\" vehicleCategory=\"car\">\n            <ParameterDeclarations/>\n            <Performance maxSpeed=\"69.444\" maxAcceleration=\"10.0\" maxDeceleration=\"10.0\"/>\n            <BoundingBox>\n              <Center x=\"1.5\" y=\"0.0\" z=\"0.9\"/>\n              <Dimensions width=\"2.1\" length=\"4.5\" height=\"1.8\"/>\n            </BoundingBox>\n            <Axles>\n              <FrontAxle maxSteering=\"0.5\" wheelDiameter=\"0.6\" trackWidth=\"1.8\" positionX=\"3.1\" positionZ=\"0.3\"/>\n              <RearAxle maxSteering=\"0.0\" wheelDiameter=\"0.6\" trackWidth=\"1.8\" positionX=\"0.0\" positionZ=\"0.3\"/>\n            </Axles>\n            <Properties>\n              <Property name=\"type\" value=\"simulation\"/>\n              <Property name=\"color\" value=\"255,0,0\"/>\n            </Properties>\n          </Vehicle>\n        </ScenarioObject>\n      </Entities>\n      <Storyboard>\n        <Init>\n          <Actions>\n            <GlobalAction>\n              <EnvironmentAction>\n                <Environment name=\"Environment1\">\n                  <TimeOfDay animation=\"false\" dateTime=\"2019-06-25T12:00:00\"/>\n                  <Weather cloudState=\"free\">\n                    <Sun intensity=\"1.0\" azimuth=\"0.0\" elevation=\"1.31\"/>\n                    <Fog visualRange=\"100000.0\"/>\n                    <Precipitation precipitationType=\"dry\" intensity=\"0.0\"/>\n                  </Weather>\n                  <RoadCondition frictionScaleFactor=\"1.0\"/>\n                </Environment>\n              </EnvironmentAction>\n            </GlobalAction>\n            <Private entityRef=\"ego_vehicle\">\n              <PrivateAction>\n                <TeleportAction>\n                  <Position>\n                    <WorldPosition x=\"30\" y=\"134\" z=\"0\" h=\"0\"/>\n                  </Position>\n                </TeleportAction>\n              </PrivateAction>\n              <PrivateAction>\n                <ControllerAction>\n                    <AssignControllerAction>\n                        <Controller name=\"EgoVehicleAgent\">\n                            <Properties>\n                                <Property name=\"module\" value=\"external_control\" />\n\n                            </Properties>\n                        </Controller>\n                    </AssignControllerAction>\n                    <OverrideControllerValueAction>\n                        <Throttle value=\"0\" active=\"false\" />\n                        <Brake value=\"0\" active=\"false\" />\n                        <Clutch value=\"0\" active=\"false\" />\n                        <ParkingBrake value=\"0\" active=\"false\" />\n                        <SteeringWheel value=\"0\" active=\"false\" />\n                        <Gear number=\"0\" active=\"false\" />\n                    </OverrideControllerValueAction>\n                </ControllerAction>\n            </PrivateAction>\n            </Private>\n            <Private entityRef=\"adversary\">\n              <PrivateAction>\n                <TeleportAction>\n                  <Position>\n                    <WorldPosition x=\"90\" y=\"134\" z=\"0\" h=\"0\"/>\n                  </Position>\n                </TeleportAction>\n              </PrivateAction>\n            </Private>\n          </Actions>\n        </Init>\n        <Story name=\"MyStory\">\n          <Act name=\"Behavior\">\n            <ManeuverGroup maximumExecutionCount=\"1\" name=\"ManeuverSequence\">\n              <Actors selectTriggeringEntities=\"false\">\n                <EntityRef entityRef=\"adversary\"/>\n              </Actors>\n              <Maneuver name=\"FollowLeadingVehicleManeuver\">\n                <Event name=\"LeadingVehicleKeepsVelocity\" priority=\"overwrite\">\n                  <Action name=\"LeadingVehicleKeepsVelocity\">\n                    <PrivateAction>\n                      <LongitudinalAction>\n                        <SpeedAction>\n                          <SpeedActionDynamics dynamicsShape=\"step\" value=\"100\" dynamicsDimension=\"distance\"/>\n                          <SpeedActionTarget>\n                            <AbsoluteTargetSpeed value=\"$leadingSpeed\"/>\n                          </SpeedActionTarget>\n                        </SpeedAction>\n                      </LongitudinalAction>\n                    </PrivateAction>\n                  </Action>\n                  <StartTrigger>\n                    <ConditionGroup>\n                      <Condition name=\"StartCondition\" delay=\"0\" conditionEdge=\"rising\">\n                        <ByEntityCondition>\n                          <TriggeringEntities triggeringEntitiesRule=\"any\">\n                            <EntityRef entityRef=\"ego_vehicle\"/>\n                          </TriggeringEntities>\n                          <EntityCondition>\n                            <RelativeDistanceCondition entityRef=\"adversary\" relativeDistanceType=\"cartesianDistance\" value=\"40.0\" freespace=\"false\" rule=\"lessThan\"/>\n                          </EntityCondition>\n                        </ByEntityCondition>\n                      </Condition>\n                    </ConditionGroup>\n                  </StartTrigger>\n                </Event>\n              </Maneuver>\n            </ManeuverGroup>\n            <StartTrigger>\n              <ConditionGroup>\n                <Condition name=\"OverallStartCondition\" delay=\"0\" conditionEdge=\"rising\">\n                  <ByEntityCondition>\n                    <TriggeringEntities triggeringEntitiesRule=\"any\">\n                      <EntityRef entityRef=\"ego_vehicle\"/>\n                    </TriggeringEntities>\n                    <EntityCondition>\n                      <TraveledDistanceCondition value=\"1.0\"/>\n                    </EntityCondition>\n                  </ByEntityCondition>\n                </Condition>\n                <Condition name=\"StartTime\" delay=\"0\" conditionEdge=\"rising\">\n                  <ByValueCondition>\n                    <SimulationTimeCondition value=\"0\" rule=\"equalTo\"/>\n                  </ByValueCondition>\n                </Condition>\n              </ConditionGroup>\n            </StartTrigger>\n            <StopTrigger>\n              <ConditionGroup>\n                <Condition name=\"EndCondition\" delay=\"0\" conditionEdge=\"rising\">\n                  <ByEntityCondition>\n                    <TriggeringEntities triggeringEntitiesRule=\"any\">\n                      <EntityRef entityRef=\"ego_vehicle\"/>\n                    </TriggeringEntities>\n                    <EntityCondition>\n                      <TraveledDistanceCondition value=\"100.0\"/>\n                    </EntityCondition>\n                  </ByEntityCondition>\n                </Condition>\n              </ConditionGroup>\n            </StopTrigger>\n          </Act>\n        </Story>\n        <StopTrigger>\n          <ConditionGroup>\n            <Condition name=\"criteria_RunningStopTest\" delay=\"0\" conditionEdge=\"rising\">\n              <ByValueCondition>\n                <ParameterCondition parameterRef=\"\" value=\"\" rule=\"lessThan\"/>\n              </ByValueCondition>\n            </Condition>\n            <Condition name=\"criteria_RunningRedLightTest\" delay=\"0\" conditionEdge=\"rising\">\n              <ByValueCondition>\n                <ParameterCondition parameterRef=\"\" value=\"\" rule=\"lessThan\"/>\n              </ByValueCondition>\n            </Condition>\n            <Condition name=\"criteria_WrongLaneTest\" delay=\"0\" conditionEdge=\"rising\">\n              <ByValueCondition>\n                <ParameterCondition parameterRef=\"\" value=\"\" rule=\"lessThan\"/>\n              </ByValueCondition>\n            </Condition>\n            <Condition name=\"criteria_OnSidewalkTest\" delay=\"0\" conditionEdge=\"rising\">\n              <ByValueCondition>\n                <ParameterCondition parameterRef=\"\" value=\"\" rule=\"lessThan\"/>\n              </ByValueCondition>\n            </Condition>\n            <Condition name=\"criteria_KeepLaneTest\" delay=\"0\" conditionEdge=\"rising\">\n              <ByValueCondition>\n                <ParameterCondition parameterRef=\"\" value=\"\" rule=\"lessThan\"/>\n              </ByValueCondition>\n            </Condition>\n            <Condition name=\"criteria_CollisionTest\" delay=\"0\" conditionEdge=\"rising\">\n              <ByValueCondition>\n                <ParameterCondition parameterRef=\"\" value=\"\" rule=\"lessThan\"/>\n              </ByValueCondition>\n            </Condition>\n            <Condition name=\"criteria_DrivenDistanceTest\" delay=\"0\" conditionEdge=\"rising\">\n              <ByValueCondition>\n                <ParameterCondition parameterRef=\"distance_success\" value=\"100\" rule=\"lessThan\"/>\n              </ByValueCondition>\n            </Condition>\n          </ConditionGroup>\n        </StopTrigger>\n      </Storyboard>\n    </OpenSCENARIO>",
        "type": "openScenario"
    }

    for scene in [scene_2, scene_3, scene_4, scene_5, scene_6_openscenario]:
        await DynamicSceneCommandUsercase(db_session=db_session, user=user).create_scenario(
            DynamicSceneCreateDTO(**scene))

    from sdgApp.Application.ScenariosFacadeService.AssembleService import AssembleScenarioService
    from sdgApp.Application.ScenariosFacadeService.CommandDTOs import AssemberScenarioCreateDTO
    from sdgApp.Application.scenarios.usercase import ScenarioQueryUsercase

    assemble_scenario = {"name": "基础场景",
                         "desc": "初始化场景，所有配置均使用简单配置，用于用户初次试用产品试用。",
                         "map_name": "Town03",
                         "dynamic_scene_id": default_scene_dto.id,
                         "weather_id": "ClearNoon",
                         "types": "file",
                         "parent_id": "root",
                         "tags": []}
    await AssembleScenarioService(AssemberScenarioCreateDTO(**assemble_scenario), db_session, user)
    default_scenario_dto = await ScenarioQueryUsercase(db_session=db_session, user=user).find_all_scenarios(1, 15, "",
                                                                                                            "")
    default_scenario_dto = default_scenario_dto["datas"][0]

    from sdgApp.Application.job.CommandDTOs import JobCreateDTO
    from sdgApp.Application.job.usercase import JobCommandUsercase
    default_task_dict = {"id": shortuuid.uuid(),
                         "name": "",
                         "desc": "",
                         "car_id": default_car_dto.id,
                         "car_name": default_car_dto.name,
                         "scenario_id": default_scenario_dto.id,
                         "scenario_name": default_scenario_dto.name}
    default_job_dict = {"name": "基础测试样例",
                        "desc": "初始化预设作业，包含一个简单场景和一个车辆，用于用户初次试用体验。",
                        "task_list": [default_task_dict]}
    await JobCommandUsercase(db_session=db_session, user=user).create_job(JobCreateDTO(**default_job_dict))
