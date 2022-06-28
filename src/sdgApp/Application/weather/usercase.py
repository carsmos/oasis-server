import math

import shortuuid
from sdgApp.Application.weather.RespondsDTOs import WeatherReadDTO
from sdgApp.Application.weather.CommandDTOs import WeatherCreateDTO, WeatherUpdateDTO
from sdgApp.Domain.weather.weathers import WeatherAggregate
from sdgApp.Domain.weather.weathers_exceptions import WeatherNotFoundError
from sdgApp.Infrastructure.MongoDB.weather.weather_repoImpl import WeatherRepoImpl
from sdgApp.Application.log.usercase import except_logger


class WeatherCommandUsercase(object):

    def __init__(self, db_session, user, repo=WeatherRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    @except_logger("create_weather failed .....................")
    async def create_weather(self, weather_create_model: WeatherCreateDTO):
        try:
            uuid = shortuuid.uuid()
            weather = WeatherAggregate(id=uuid,
                                name=weather_create_model.name,
                                desc=weather_create_model.desc,
                                param=weather_create_model.param)
            await self.repo.create_weather(weather)
        except:
            raise

    @except_logger("delete_weather failed .....................")
    async def delete_weather(self, weather_ids: str):
        try:
            for weather_id in weather_ids.split("+"):
                await self.repo.delete_weather(weather_id)
        except:
            raise

    @except_logger("update_weather failed .....................")
    async def update_weather(self, weather_id: str, weather_create_model: WeatherUpdateDTO):
        try:
            weather_retrieved = await self.repo.get(weather_id)
            weather_retrieved.name = weather_create_model.name
            weather_retrieved.desc = weather_create_model.desc
            weather_retrieved.param = weather_create_model.param
            await self.repo.update_weather(weather_id, weather_retrieved)
        except:
            raise


class WeatherQueryUsercase(object):

    def __init__(self, db_session, user, ):
        self.db_session = db_session
        self.user = user
        self.weather_collection = self.db_session['weather']

    @except_logger("find_specified_weather failed .....................")
    async def find_specified_weather(self, weather_id: str):
        try:
            filter = {'id': weather_id}
            filter.update({"usr_id": self.user.id})
            result_dict = await self.weather_collection.find_one(filter, {'_id': 0})
            if result_dict is None:
                raise WeatherNotFoundError
            return WeatherReadDTO(**result_dict)
        except:
            raise

    @except_logger("find_all_weather failed .....................")
    async def find_all_weather(self, p_num, p_size, content):
        try:
            filter = ({"usr_id": self.user.id})
            if content not in [""]:
                filter.update({"$or": [{"name": {"$regex": content, "$options": "i"}},
                                       {"desc": {"$regex": content, "$options": "i"}}]})
            total_num = await self.weather_collection.count_documents(filter)
            total_page_num = math.ceil(total_num / p_size)
            if p_num > total_page_num and total_page_num > 0:
                p_num = total_page_num
            if p_num > 0:
                results_dict = self.weather_collection.find(filter, {'_id': 0}).sort(
                    [('last_modified', -1)]).skip((p_num - 1) * p_size).limit(p_size).to_list(length=50)
            else:
                results_dict = self.weather_collection.find(filter, {'_id': 0}).sort(
                    [('last_modified', -1)]).to_list(length=total_num)
            if results_dict:
                response_dic = {}
                response_dto_lst = []
                response_dic["total_num"] = total_num
                response_dic["total_page_num"] = total_page_num

                for doc in await results_dict:
                    response_dto_lst.append(WeatherReadDTO(**doc))
                response_dic["datas"] = response_dto_lst
                return response_dic
        except:
            raise
