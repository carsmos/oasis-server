import shortuuid

from sdgApp.Application.car.CommandDTOs import CarCreateDTO, CarUpdateDTO
from sdgApp.Domain.car.car import CarAggregate
from sdgApp.Infrastructure.MongoDB.car.car_repoImpl import CarRepoImpl


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
            car = CarAggregate(uuid,
                               name=car_dict["name"],
                               desc=car_dict["desc"],
                               param=car_dict["param"])
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
            car_update_dict = dto
            update_car = CarAggregate(car_id,
                                      name=car_update_dict["name"],
                                      desc=car_update_dict["desc"],
                                      param=car_update_dict["param"])
            self.repo.update(update_car)

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
            self.repo.update_snap(snapshot_car)

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

