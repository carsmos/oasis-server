from datetime import datetime

from sdgApp.Domain.sensor.sensor import SensorAggregate
from sdgApp.Domain.sensor.sensor_repo import SensorRepo


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    ...


class SensorRepoImpl(SensorRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.sensor_collection = self.db_session['sensors']

    def create(self, sensor: SensorAggregate):
        sensor_DO = {"id": sensor.id,
                     "name": sensor.name,
                     "type": sensor.type,
                     "car_id": sensor.car_id,
                     "car_name": sensor.car_name,
                     "desc": sensor.desc,
                     "param": sensor.param}
        sensor_DO.update({"usr_id": self.user.id})
        sensor_DO.update({"create_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       "last_modified": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

        self.sensor_collection.insert_one(sensor_DO)

    def delete(self, sensor_id: str):
        filter = {'id': sensor_id}
        filter.update({"usr_id": self.user.id})

        self.sensor_collection.delete_one(filter)

    def update(self, update_sensor: SensorAggregate):
        update_sensor_DO = {"name": update_sensor.name,
                            "type": update_sensor.type,
                            "car_id": update_sensor.car_id,
                            "car_name": update_sensor.car_name,
                            "desc": update_sensor.desc,
                            "param": update_sensor.param}
        update_sensor_DO.update({"last_modified": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

        filter = {
            'id': update_sensor.id
        }
        filter.update({"usr_id": self.user.id})

        self.sensor_collection.update_one(filter
                                           , {'$set': update_sensor_DO})

    def get(self, sensor_id: str):
        filter = {'id': sensor_id}
        filter.update({"usr_id": self.user.id})

        result_DO = self.sensor_collection.find_one(filter, {'_id': 0, 'usr_id': 0})
        if result_DO:
            sensor = SensorAggregate(id=result_DO["id"])
            sensor.save_DO_shortcut(result_DO)
            return sensor

    def list(self, query_param: dict):
        filter = {"usr_id": self.user.id}
        filter.update(query_param)

        sensor_aggregate_lst = []
        results_DO = self.sensor_collection.find(filter, {'_id': 0, 'usr_id': 0})
        if results_DO:
            for one_result in results_DO:
                one_sensor = SensorAggregate(id=one_result["id"])
                one_sensor.save_DO_shortcut(one_result)
                sensor_aggregate_lst.append(one_sensor)
            return sensor_aggregate_lst
