import math

import shortuuid

from sdgApp.Application.car.usercase import split_page
from sdgApp.Application.sensor.CommandDTOs import SensorCreateDTO, SensorUpdateDTO
from sdgApp.Application.sensor.RespondsDTOs import SensorReadDTO
from sdgApp.Domain.sensor.sensor import SensorAggregate
from sdgApp.Domain.sensor.sensor_exceptions import SensorNotFoundError
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
            sensor_retrieved = await self.repo.get(sensor_id=sensor_id)
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
            if result_dict is None:
                raise SensorNotFoundError
            return SensorReadDTO(**result_dict)
        except:
            raise

    async def list_sensor(self, p_num, limit, query_param: dict):
        try:
            filter = {"usr_id": self.user.id}
            content = query_param.get("content")
            if content:
                filter.update({"$or": [{"name": {"$regex": content}}, {"desc": {"$regex": content}}]})
                query_param.pop("content")

            filter.update(query_param)

            total_num = await self.sensor_collection.count_documents(filter)
            total_page_num = math.ceil(total_num / limit)
            if p_num > total_page_num and total_page_num > 0:
                p_num = total_page_num
            if p_num > 0:
                results_dict = self.sensor_collection.find(filter, {'_id': 0, 'usr_id':0}).sort([('last_modified', -1)]).skip((p_num-1) * limit).limit(limit).to_list(length=50)
            else:
                results_dict = self.sensor_collection.find(filter, {'_id': 0, 'usr_id':0}).sort([('last_modified', -1)]).to_list(length=total_num)
            if results_dict:
                response_dic = {}
                response_dto_lst = []
                response_dic["total_num"] = total_num
                response_dic["total_page_num"] = total_page_num

                for doc in await results_dict:
                    response_dto_lst.append(SensorReadDTO(**doc))
                response_dic["datas"] = response_dto_lst
                return response_dic
        except:
            raise

