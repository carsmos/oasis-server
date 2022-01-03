from sdgApp.Application.cars.CommandDTOs import CarCreateDTO, CarUpdateDTO, CarDeleteDTO
from sdgApp.Domain.cars.cars import CarsAggregate
from sdgApp.Infrastructure.MongoDB.car.car_repoImpl import CarRepoImpl
from sdgApp.Infrastructure.MongoDB.session_maker import mongo_session
import shortuuid
from fastapi import Depends
from collections import OrderedDict

class CarCommandUsercase(object):

    def __init__(self, repo=CarRepoImpl, db_session=mongo_session):
        self.repo = repo
        _, db = db_session()
        self.repo = self.repo(db)

    def create_car(self, dto: CarCreateDTO):
        try:
            uuid = shortuuid.uuid()
            car_dict = dto.dict()
            car = CarsAggregate(id=str(uuid),
                                name=car_dict['name'],
                                autosys=car_dict['autosys'],
                                model_dict=car_dict['model'],
                                physics_dict=car_dict['physics'],
                                wheels_dict=car_dict['wheels'],
                                sensors_list=car_dict['sensors'],
                                desc=car_dict['desc'])
            car.save_DO_shortcut(car_dict)
            self.repo.create(car)
        except:
            raise




