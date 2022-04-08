import shortuuid

from sdgApp.Application.car.usercase import split_page
from sdgApp.Application.sensor.CommandDTOs import SensorCreateDTO, SensorUpdateDTO
from sdgApp.Application.sensor.RespondsDTOs import SensorReadDTO
from sdgApp.Domain.sensor.sensor import SensorAggregate
from sdgApp.Infrastructure.MongoDB.sensor.sensor_repoImpl import SensorRepoImpl


class SensorCommandUsercase(object):

    def __init__(self, db_session, user, repo=SensorRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    async def create_sensor(self, sensor_create_model: SensorCreateDTO):
        try:
            uuid = shortuuid.uuid()

            sensor = SensorAggregate(id=uuid,
                                name=sensor_create_model.name,
                                type=sensor_create_model.type,
                                desc=sensor_create_model.desc,
                                param=sensor_create_model.param)
            await self.repo.create(sensor)

        except:
            raise

    async def delete_sensor(self, sensor_id: str):
        try:
            await self.repo.delete(sensor_id)
        except:
            raise

    async def update_sensor(self, sensor_id:str, sensor_update_model: SensorUpdateDTO):
        try:
            sensor_retrieved = self.repo.get(sensor_id=sensor_id)
            sensor_retrieved.name = sensor_update_model.name
            sensor_retrieved.type = sensor_update_model.type
            sensor_retrieved.param = sensor_update_model.param
            sensor_retrieved.desc = sensor_update_model.desc

            await self.repo.update(sensor_retrieved)

        except:
            raise


class SensorQueryUsercase(object):

    def __init__(self, db_session, user, repo=SensorRepoImpl):
        self.db_session = db_session
        self.user = user
        self.sensor_collection = self.db_session['sensors']

    async def get_sensor(self, sensor_id:str):
        try:
            filter = {'id': sensor_id}
            filter.update({"usr_id": self.user.id})
            result_dict = await self.sensor_collection.find_one(filter, {'_id': 0, 'usr_id': 0})
            return SensorReadDTO(**result_dict)
        except:
            raise

    async def list_sensor(self, p_num, query_param: dict):
        try:
            response_dto_lst = []
            filter = {"usr_id": self.user.id}
            filter.update(query_param)

            results_dict = self.sensor_collection.find(filter, {'_id': 0, 'usr_id':0}).sort([('last_modified', -1)])
            if results_dict:
                async for one_result in results_dict:
                    response_dto_lst.append(SensorReadDTO(**one_result))

                response_dto_lst = split_page(p_num, response_dto_lst)
                return response_dto_lst
        except:
            raise

