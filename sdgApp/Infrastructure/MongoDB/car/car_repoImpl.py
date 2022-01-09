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


        car_DO = {"id": car.id,
                  "name": car.name,
                  "desc": car.desc,
                  "param": car.param}

        self.cars_collection.insert_one(car_DO)

    def delete(self, car_id: str):
        filter = {'id': car_id}
        self.cars_collection.delete_one(filter)

    def update(self, update_car: CarsAggregate):
        update_car_DO = {"name": update_car.name,
                  "desc": update_car.desc,
                  "param": update_car.param}

        filter = {
                'id': update_car.id
            }
        self.cars_collection.update_one(filter
            , {'$set': update_car_DO})

    def get(self, car_id: str):
        filter = {'id': car_id}
        result_DO = self.cars_collection.find_one(filter, {'_id':0})
        car = CarsAggregate(id=result_DO["id"])
        car.save_DO_shortcut(result_DO)
        return car

    def list(self):
        car_aggregate_lst = []
        results_DO = self.cars_collection.find({}, {'_id':0})
        for one_result in results_DO:
            one_car = CarsAggregate(id=one_result["id"])
            one_car.save_DO_shortcut(one_result)
            car_aggregate_lst.append(one_car)
        return car_aggregate_lst






