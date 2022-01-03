from sdgApp.Domain.cars.cars_repo import CarsRepo
from sdgApp.Domain.cars.cars import CarsAggregate

def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO

def DataMapper_to_Aggregate(DO):
    ...

class CarRepoImpl(CarsRepo):

    def __init__(self, db_session):
        self.db_session = db_session
        self.cars_collection = self.db_session['cars']

    def create(self, car: CarsAggregate):
        car_DO = DataMapper_to_DO(car)
        self.cars_collection.insert_one(car_DO)

    # def find_by_id(self, id: str):
    #     query = {"id": id}
    #     car_DO = self.cars_collection.find(query, {"_id": 0})







