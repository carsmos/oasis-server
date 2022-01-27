import shortuuid
import copy

from sdgApp.Application.car.CommandDTOs import CarCreateDTO, CarUpdateDTO
from sdgApp.Domain.car.car import CarAggregate
from sdgApp.Infrastructure.MongoDB.car.car_repoImpl import CarRepoImpl


DEFAULT_SENSORS_SNAP = {'car_id':'',
                        'car_name':'',
                        "sensors": [
	{
		"default":"1",
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
		"sensor_id": "001",
		"sensor_name": "default_cam"
	}, {
		"default":"1",
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
		"sensor_id": "002",
		"sensor_name": "default_lidar"
	},
]}

DEFAULT_CAR_SNAP = {'car_id':'',
                    'car_name':'',
                    'vehicle_physics_control': {
                                'dynamics_id': '',
                                'dynamics_name': '',
                                'wheels': {
                                    'front_left_wheel': {
                                        'wheel_id': '',
                                        'wheel_name': '',
                                        'position': ''
                                    },
                                    'front_right_wheel': {
                                        'wheel_id': '',
                                        'wheel_name': '',
                                        'position': ''
                                    },
                                    'rear_left_wheel': {
                                        'wheel_id': '',
                                        'wheel_name': '',
                                        'position': ''
                                    },
                                    'rear_right_wheel': {
                                        'wheel_id': '',
                                        'wheel_name': '',
                                        'position': ''
                                    }
                                  }
                                }
                    }


def dto_assembler(car: CarAggregate):
    return car.shortcut_DO

class CarCommandUsercase(object):

    def __init__(self, db_session, user, repo=CarRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def create_car(self, dto: dict):
        try:
            uuid = shortuuid.uuid()
            car_dict = dto

            COPY_CAR_SNAP = copy.deepcopy(DEFAULT_CAR_SNAP)
            COPY_SENSORS_SNAP = copy.deepcopy(DEFAULT_SENSORS_SNAP)

            COPY_CAR_SNAP['car_id'] = uuid
            COPY_CAR_SNAP['car_name'] = car_dict["name"]
            COPY_CAR_SNAP.update(car_dict["param"])

            COPY_SENSORS_SNAP['car_id'] = uuid
            COPY_SENSORS_SNAP['car_name'] = car_dict["name"]

            car = CarAggregate(uuid,
                               name=car_dict["name"],
                               desc=car_dict["desc"],
                               param=car_dict["param"],
                               sensors_snap=COPY_SENSORS_SNAP,
                               car_snap=COPY_CAR_SNAP)
            self.repo.create(car)

            car = self.repo.get(car_id=uuid)
            if car:
                response_dto = dto_assembler(car)
                return response_dto

        except:
            raise

    def delete_car(self, car_id: str):
        try:
            self.repo.delete(car_id)
        except:
            raise

    def update_car(self, car_id:str, dto: dict):
        try:
            car_retrieved = self.repo.get(car_id=car_id)
            car_update_dict = dto

            car_retrieved.name = car_update_dict["name"]
            car_retrieved.desc = car_update_dict["desc"]
            car_retrieved.param = car_update_dict["param"]
            car_retrieved.car_snap.update(car_update_dict["param"])
            car_retrieved.car_snap['car_name'] = car_update_dict["name"]
            car_retrieved.sensors_snap['car_name'] = car_update_dict["name"]

            self.repo.update(car_retrieved)

            car = self.repo.get(car_id=car_id)
            if car:
                response_dto = dto_assembler(car)
                return response_dto
        except:
            raise

    def update_car_snap(self, car_id:str, dto: dict):
        try:
            car_snap_dict = dto
            snapshot_car = CarAggregate(car_id,
                                        name=car_snap_dict["name"],
                                        desc=car_snap_dict["desc"],
                                        param=car_snap_dict["param"],
                                        sensors_snap=car_snap_dict["sensors_snap"],
                                        car_snap=car_snap_dict["car_snap"])
            self.repo.update(snapshot_car)

            car = self.repo.get(car_id=car_id)
            if car:
                response_dto = dto_assembler(car)
                return response_dto

        except:
            raise




class CarQueryUsercase(object):

    def __init__(self, db_session, user, repo=CarRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def get_car(self, car_id:str):
        try:
            car = self.repo.get(car_id)
            if car:
                response_dto = dto_assembler(car)
                return response_dto
        except:
            raise

    def list_car(self):
        try:
            response_dto_lst = []
            car_lst = self.repo.list()
            if car_lst:
                for car in car_lst:
                    response_dto = dto_assembler(car)
                    response_dto_lst.append(response_dto)
                return response_dto_lst
        except:
            raise

