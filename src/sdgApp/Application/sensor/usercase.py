import shortuuid

from sdgApp.Application.sensor.CommandDTOs import SensorCreateDTO, SensorUpdateDTO
from sdgApp.Domain.sensor.sensor import SensorAggregate
from sdgApp.Infrastructure.MongoDB.sensor.sensor_repoImpl import SensorRepoImpl


def dto_assembler(sensor: SensorAggregate):
    return sensor.shortcut_DO

class SensorCommandUsercase(object):

    def __init__(self, db_session, user, repo=SensorRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def create_sensor(self, dto: dict):
        try:
            uuid = shortuuid.uuid()
            sensor_dict = dto
            sensor = SensorAggregate(id=uuid,
                                name=sensor_dict["name"],
                                type=sensor_dict["type"],
                                car_name=sensor_dict["car_name"],
                                car_id=sensor_dict["car_id"],
                                desc=sensor_dict["desc"],
                                param=sensor_dict["param"])
            self.repo.create(sensor)

            sensor = self.repo.get(sensor_id=uuid)
            if sensor:
                response_dto = dto_assembler(sensor)
                return response_dto
        except:
            raise

    def delete_sensor(self, sensor_id: str):
        try:
            self.repo.delete(sensor_id)
        except:
            raise

    def update_sensor(self, sensor_id:str, dto: dict):
        try:
            sensor_update_dict = dto
            update_sensor = SensorAggregate(sensor_id,
                                            name=sensor_update_dict["name"],
                                            type=sensor_update_dict["type"],
                                            car_name=sensor_update_dict["car_name"],
                                            car_id=sensor_update_dict["car_id"],
                                            desc=sensor_update_dict["desc"],
                                            param=sensor_update_dict["param"])
            self.repo.update(update_sensor)

            sensor = self.repo.get(sensor_id=sensor_id)
            if sensor:
                response_dto = dto_assembler(sensor)
                return response_dto
        except:
            raise


class SensorQueryUsercase(object):

    def __init__(self, db_session, user, repo=SensorRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def get_sensor(self, sensor_id:str):
        try:
            sensor = self.repo.get(sensor_id)
            if sensor:
                response_dto = dto_assembler(sensor)
                return response_dto
        except:
            raise

    def list_sensor(self, query_param: dict):
        try:
            response_dto_lst = []
            sensor_lst = self.repo.list(query_param=query_param)
            if sensor_lst:
                for sensor in sensor_lst:
                    response_dto = dto_assembler(sensor)
                    response_dto_lst.append(response_dto)
                return response_dto_lst
        except:
            raise
