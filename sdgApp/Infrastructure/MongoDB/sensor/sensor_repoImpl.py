from sdgApp.Domain.sensor.sensor import SensorAggregate
from sdgApp.Domain.sensor.sensor_repo import SensorRepo


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    ...


class SensorRepoImpl(SensorRepo):

    def __init__(self, db_session):
        self.db_session = db_session
        self.sensors_collection = self.db_session['sensors']

    def create(self, sensor: SensorAggregate):
        sensor_DO = {"id": sensor.id,
                     "name": sensor.name,
                     "car_id": sensor.car_id,
                     "car_name": sensor.car_name,
                     "desc": sensor.desc,
                     "param": sensor.param}

        self.sensors_collection.insert_one(sensor_DO)

    def delete(self, sensor_id: str):
        filter = {'id': sensor_id}
        self.sensors_collection.delete_one(filter)

    def update(self, update_sensor: SensorAggregate):
        update_sensor_DO = {"name": update_sensor.name,
                            "car_id": update_sensor.car_id,
                            "car_name": update_sensor.car_name,
                            "desc": update_sensor.desc,
                            "param": update_sensor.param}

        filter = {
            'id': update_sensor.id
        }
        self.sensors_collection.update_one(filter
                                           , {'$set': update_sensor_DO})

    def get(self, sensor_id: str):
        filter = {'id': sensor_id}
        result_DO = self.sensors_collection.find_one(filter, {'_id': 0})
        sensor = SensorAggregate(id=result_DO["id"])
        sensor.save_DO_shortcut(result_DO)
        return sensor

    def list(self):
        sensor_aggregate_lst = []
        results_DO = self.sensors_collection.find({}, {'_id': 0})
        for one_result in results_DO:
            one_sensor = SensorAggregate(id=one_result["id"])
            one_sensor.save_DO_shortcut(one_result)
            sensor_aggregate_lst.append(one_sensor)
        return sensor_aggregate_lst
