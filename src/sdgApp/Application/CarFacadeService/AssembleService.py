import copy

from sdgApp.Application.car.usercase import CarCommandUsercase, CarQueryUsercase
from sdgApp.Application.CarFacadeService.CommandDTOs import AssembleCreateDTO
from sdgApp.Application.car.CommandDTOs import CarCreateDTO, CarUpdateDTO
from sdgApp.Application.car.RespondsDTOs import CarReadDTO
from sdgApp.Application.dynamics.usercase import DynamicsQueryUsercase
from sdgApp.Application.sensor.usercase import SensorQueryUsercase

DEFAULT_SENSORS_SNAP = {'car_id': '',
                        'car_name': '',
                        "sensors": [
                            {
                                "type": "sensor.camera.rgb",
                                "id": "view",
                                "position": ["-4.5", "0", "2.8"],
                                "roll": 0,
                                "pitch": -20,
                                "yaw": 0,
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
                                "sensor_name": "default_cam"
                            }, {
                                "type": "sensor.lidar.ray_cast",
                                "id": "lidar1",
                                "position": ["0", "0", "2.4"],
                                "roll": 0,
                                "pitch": 0,
                                "yaw": 0,
                                "range": 50,
                                "channels": 32,
                                "points_per_second": 320000,
                                "upper_fov": 2,
                                "lower_fov": -26.8,
                                "rotation_frequency": 20,
                                "sensor_tick": 0.05,
                                "noise_stddev": 0,
                                "sensor_id": "default",
                                "sensor_name": "default_lidar"
                            },
                        ]}


async def AssembleCarService(assemble_create_model: AssembleCreateDTO, db_session, user, overview_only=False):
    dynamics_id = assemble_create_model.dynamics_id
    sensors = assemble_create_model.sensors

    car_snap_dict = {}
    sensors_snap_dict = copy.deepcopy(DEFAULT_SENSORS_SNAP)

    car_snap_dict.update(assemble_create_model.param)

    if dynamics_id:
        dynamics_dto = await DynamicsQueryUsercase(db_session=db_session, user=user).get_dynamics(dynamics_id)
        if dynamics_dto:
            dynamics_dto.param["dynamics_id"] = dynamics_id
            dynamics_dto.param["dynamics_name"] = dynamics_dto.name
            car_snap_dict["vehicle_physics_control"] = dynamics_dto.param

    if sensors:
        for sensor_info_dict in sensors:
            sensor_id = sensor_info_dict["id"]
            sensor_position = sensor_info_dict.get("position")
            sensor_dto = await SensorQueryUsercase(db_session=db_session, user=user).get_sensor(sensor_id)
            if sensor_dto:
                sensor_dto.param["sensor_id"] = sensor_id
                sensor_dto.param["sensor_name"] = sensor_dto.name
                sensor_dto.param["position"] = sensor_position
                sensor_dto.param["type"] = sensor_dto.type
                sensors_snap_dict["sensors"].append(sensor_dto.param)

    if overview_only:
        if not assemble_create_model.id:
            return CarReadDTO(id="",
                              name=assemble_create_model.name,
                              desc=assemble_create_model.desc,
                              param=assemble_create_model.param,
                              car_snap=car_snap_dict,
                              sensors_snap=sensors_snap_dict,
                              create_time="",
                              last_modified=""
                              )
        else:
            car_dto = await CarQueryUsercase(db_session=db_session, user=user).get_car(assemble_create_model.id)
            return CarReadDTO(id=assemble_create_model.id,
                              name=assemble_create_model.name,
                              desc=assemble_create_model.desc,
                              param=assemble_create_model.param,
                              car_snap=car_snap_dict,
                              sensors_snap=sensors_snap_dict,
                              create_time=car_dto.create_time,
                              last_modified=car_dto.last_modified
                              )

    if not assemble_create_model.id:

        car_creata_model = CarCreateDTO(name=assemble_create_model.name,
                                        desc=assemble_create_model.desc,
                                        param=assemble_create_model.param,
                                        car_snap=car_snap_dict,
                                        sensors_snap=sensors_snap_dict)
        await CarCommandUsercase(db_session=db_session, user=user).create_car(car_creata_model)

    else:

        car_update_model = CarUpdateDTO(name=assemble_create_model.name,
                                        desc=assemble_create_model.desc,
                                        param=assemble_create_model.param,
                                        car_snap=car_snap_dict,
                                        sensors_snap=sensors_snap_dict)
        await CarCommandUsercase(db_session=db_session, user=user).update_car(assemble_create_model.id,
                                                                        car_update_model)
