from sdgApp.Application.car.usercase import CarCommandUsercase, CarQueryUsercase
from sdgApp.Application.dynamics.usercase import DynamicsQueryUsercase
from sdgApp.Application.wheel.usercase import WheelQueryUsercase
from sdgApp.Application.sensor.usercase import SensorQueryUsercase



def AssembleCarService(assemble_create_dto: dict, db_session, user):
    car_id_with_extraconfig = assemble_create_dto["car_id_with_extraconfig"]
    dynamics_id_with_extraconfig = assemble_create_dto["dynamics_id_with_extraconfig"]
    wheel_id_with_extraconfig = assemble_create_dto["wheel_id_with_extraconfig"]
    sensor_id_with_extraconfig = assemble_create_dto["sensor_id_with_extraconfig"]

    for car_id, car_extra_config in car_id_with_extraconfig.items():
        car_snapshot_dto = CarQueryUsercase(db_session=db_session, user=user).get_car(car_id)
        car_snapshot_dto["param"].update(car_extra_config)

    car_snapshot_dto["param"]["dynamics"] = {}
    car_snapshot_dto["param"]["wheels"] = []
    car_snapshot_dto["param"]["sensors"] = []

    for dynamics_id, dynamics_extra_config in dynamics_id_with_extraconfig.items():
        dynamics_dto = DynamicsQueryUsercase(db_session=db_session, user=user).get_dynamics(dynamics_id)
        dynamics_dto["param"].update(dynamics_extra_config)
        car_snapshot_dto["param"]["dynamics"].update(dynamics_dto["param"])

    for wheel_id, wheel_extra_config in wheel_id_with_extraconfig.items():
        wheel_dto = WheelQueryUsercase(db_session=db_session, user=user).get_wheel(wheel_id)
        wheel_dto["param"].update(wheel_extra_config)
        car_snapshot_dto["param"]["wheels"].append(wheel_dto["param"])

    for sensor_id, sensor_extra_config in sensor_id_with_extraconfig.items():
        sensor_dto = SensorQueryUsercase(db_session=db_session, user=user).get_sensor(sensor_id)
        sensor_dto["param"].update(sensor_extra_config)
        car_snapshot_dto["param"]["sensors"].append(sensor_dto["param"])

    return CarCommandUsercase(db_session=db_session, user=user).update_car(car_id=car_snapshot_dto["id"],
                                                                    dto=car_snapshot_dto)






