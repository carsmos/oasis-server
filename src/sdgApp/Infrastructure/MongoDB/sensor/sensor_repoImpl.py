from datetime import datetime

from sdgApp.Domain.sensor.sensor import SensorAggregate
from sdgApp.Domain.sensor.sensor_repo import SensorRepo
from sdgApp.Infrastructure.MongoDB.sensor.Sensor_DO import SensorDO


class SensorRepoImpl(SensorRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.sensor_collection = self.db_session['sensors']

    def create(self, sensor: SensorAggregate):
        sensor_DO = SensorDO(id=sensor.id,
                             name=sensor.name,
                             type=sensor.type,
                             desc=sensor.desc,
                             param=sensor.param,
                             usr_id=self.user.id,
                             create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                             last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        self.sensor_collection.insert_one(sensor_DO.dict())

    def delete(self, sensor_id: str):
        filter = {'id': sensor_id}
        filter.update({"usr_id": self.user.id})

        self.sensor_collection.delete_one(filter)

    def update(self, update_sensor: SensorAggregate):
        update_sensor_DO = SensorDO(id=update_sensor.id,
                                    name=update_sensor.name,
                                    type=update_sensor.type,
                                    desc=update_sensor.desc,
                                    param=update_sensor.param,
                                    usr_id=None,
                                    create_time=None,
                                    last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        filter = {
            'id': update_sensor.id
        }
        filter.update({"usr_id": self.user.id})

        self.sensor_collection.update_one(filter
                                           , {'$set': update_sensor_DO.dict(exclude_none=True)})

    def get(self, sensor_id: str):
        filter = {'id': sensor_id}
        filter.update({"usr_id": self.user.id})

        result_dict = self.sensor_collection.find_one(filter, {'_id': 0})
        if result_dict:
            sensor = SensorDO(**result_dict).to_entity()
            return sensor

    def list(self, query_param: dict):
        filter = {"usr_id": self.user.id}
        filter.update(query_param)

        sensor_aggregate_lst = []
        results_dict = self.sensor_collection.find(filter, {'_id': 0})
        if results_dict:
            for one_result in results_dict:
                one_sensor = SensorDO(**one_result).to_entity()
                sensor_aggregate_lst.append(one_sensor)
            return sensor_aggregate_lst
