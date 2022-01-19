import copy

from sdgApp.Application.car.usercase import CarCommandUsercase, CarQueryUsercase, DEFAULT_SENSORS_SNAP, DEFAULT_CAR_SNAP
from sdgApp.Application.dynamics.usercase import DynamicsQueryUsercase
from sdgApp.Application.wheel.usercase import WheelQueryUsercase
from sdgApp.Application.sensor.usercase import SensorQueryUsercase



def AssembleCarService(assemble_create_dto: dict, db_session, user):
    car_id = assemble_create_dto["car_id"]
    dynamics_id = assemble_create_dto["dynamics_id"]
    wheels = assemble_create_dto["wheels"]
    sensors = assemble_create_dto["sensors"]

    car_snapshot_dto = CarQueryUsercase(db_session=db_session, user=user).get_car(car_id)
    car_name = car_snapshot_dto["name"]

    ## reset
    COPY_CAR_SNAP = copy.deepcopy(DEFAULT_CAR_SNAP)
    COPY_SENSORS_SNAP = copy.deepcopy(DEFAULT_SENSORS_SNAP)
    car_snapshot_dto["car_snap"] = COPY_CAR_SNAP
    car_snapshot_dto["sensors_snap"] = COPY_SENSORS_SNAP

    ## car_snap init
    car_snapshot_dto["car_snap"]["car_id"] = car_id
    car_snapshot_dto["car_snap"]["car_name"] = car_name
    car_snapshot_dto["car_snap"].update(car_snapshot_dto["param"])


    ## sensors_snap init
    car_snapshot_dto["sensors_snap"]["car_id"] = car_id
    car_snapshot_dto["sensors_snap"]["car_name"] = car_name



    if dynamics_id:
        dynamics_dto = DynamicsQueryUsercase(db_session=db_session, user=user).get_dynamics(dynamics_id)
        if dynamics_dto:
            dynamics_dto["param"]["dynamics_id"] = dynamics_id
            dynamics_dto["param"]["dynamics_name"] = dynamics_dto["name"]
            car_snapshot_dto["car_snap"]["vehicle_physics_control"].update(dynamics_dto["param"])

    if wheels:
        for wheel_type, wheel_info_dict in wheels.items():
            wheel_id = wheel_info_dict["id"]
            wheel_position = wheel_info_dict["position"]
            wheel_dto = WheelQueryUsercase(db_session=db_session, user=user).get_wheel(wheel_id)
            if wheel_dto:
                wheel_dto["param"]["wheel_id"] = wheel_id
                wheel_dto["param"]["wheel_name"] = wheel_dto["name"]
                wheel_dto["param"]["position"] = wheel_position
                car_snapshot_dto["car_snap"]["vehicle_physics_control"]["wheels"].update({wheel_type:wheel_dto["param"]})

    if sensors:
        for sensor_info_dict in sensors:
            sensor_id = sensor_info_dict["id"]
            sensor_position = sensor_info_dict["position"]
            sensor_dto = SensorQueryUsercase(db_session=db_session, user=user).get_sensor(sensor_id)
            if sensor_dto:
                sensor_dto["param"]["sensor_id"] = sensor_id
                sensor_dto["param"]["sensor_name"] = sensor_dto["name"]
                sensor_dto["param"]["position"] = sensor_position
                sensor_dto["param"]["type"] = sensor_dto["type"]
                car_snapshot_dto["sensors_snap"]["sensors"].append(sensor_dto["param"])

    return CarCommandUsercase(db_session=db_session, user=user).update_car_snap(car_id=car_id,
                                                                           dto=car_snapshot_dto)





