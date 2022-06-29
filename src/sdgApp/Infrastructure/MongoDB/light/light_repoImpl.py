from datetime import datetime
from sdgApp.Infrastructure.MongoDB.light.light_DO import lightDO
from sdgApp.Domain.light.lights_repo import LightRepo
from sdgApp.Domain.light.lights import LightAggregate
from fastapi import HTTPException


class LightRepoImpl(LightRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.light_collection = self.db_session['light']

    async def create_light(self, light: LightAggregate):
        light_DO = lightDO(id=light.id,
                       name=light.name,
                       desc=light.desc,
                       param=light.param,
                       usr_id=self.user.id,
                       create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                       )
        await self.light_collection.insert_one(light_DO.dict())
        return light.id

    async def delete_light(self, light_id: str):
        filter = {'id': light_id}
        filter.update({"usr_id": self.user.id})
        await self.light_collection.delete_one(filter)

    async def update_light(self, light_id: str, light: LightAggregate):
        update_light_DO = lightDO(id=light.id,
                              name=light.name,
                              desc=light.desc,
                              param=light.param,
                              usr_id=None,
                              create_time=None,
                              last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                              )
        filter = {'id': light_id}
        filter.update({"usr_id": self.user.id})
        await self.light_collection.update_one(filter, {'$set': update_light_DO.dict(exclude={'usr_id', 'create_time'})})

    async def get(self, light_id: str):
        filter = {'id': light_id}
        filter.update({"usr_id": self.user.id})
        result_dict = await self.light_collection.find_one(filter, {'_id': 0})
        if result_dict:
            light = lightDO(**result_dict).to_entity()
            return light

    async def list(self):
        filter = {}
        filter.update({"usr_id": self.user.id})
        light_list = []
        results_dict = self.light_collection.find(filter, {'_id': 0})
        if results_dict:
            async for one_result in results_dict:
                one_light = lightDO(**one_result).to_entity()
                light_list.append(one_light)
            return light_list

