from datetime import datetime
from sdgApp.Infrastructure.MongoDB.weather.weather_DO import weatherDO
from sdgApp.Domain.weather.weathers_repo import WeatherRepo
from sdgApp.Domain.weather.weathers import WeatherAggregate
from fastapi import HTTPException


class WeatherRepoImpl(WeatherRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.weather_collection = self.db_session['weather']

    async def create_weather(self, env: WeatherAggregate):
        weather_DO = weatherDO(id=env.id,
                       name=env.name,
                       desc=env.desc,
                       param=env.param,
                       usr_id=self.user.id,
                       create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                       )
        await self.weather_collection.insert_one(weather_DO.dict())

    async def delete_weather(self, weather_id: str):
        filter = {'id': weather_id}
        filter.update({"usr_id": self.user.id})
        await self.weather_collection.delete_one(filter)

    async def update_weather(self, weather_id: str, env: WeatherAggregate):
        update_weather_DO = weatherDO(id=env.id,
                              name=env.name,
                              desc=env.desc,
                              param=env.param,
                              usr_id=None,
                              create_time=None,
                              last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                              )
        filter = {'id': weather_id}
        filter.update({"usr_id": self.user.id})
        await self.weather_collection.update_one(filter, {'$set': update_weather_DO.dict(exclude={'usr_id', 'create_time'})})

    async def get(self, weather_id: str):
        filter = {'id': weather_id}
        filter.update({"usr_id": self.user.id})
        result_dict = await self.weather_collection.find_one(filter, {'_id': 0})
        if result_dict:
            weather = weatherDO(**result_dict).to_entity()
            return weather

    async def list(self):
        filter = {}
        filter.update({"usr_id": self.user.id})
        weather_list = []
        results_dict = self.weather_collection.find(filter, {'_id': 0})
        if results_dict:
            async for one_result in results_dict:
                one_env = weatherDO(**one_result).to_entity()
                weather_list.append(one_env)
            return weather_list

