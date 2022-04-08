

class ResourceQueryUsercase(object):
    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user

        self.dynamics = self.db_session['dynamics']
        self.dynamic_scenes = self.db_session['dynamic_scenes']
        self.environments = self.db_session['environments']
        self.sensors = self.db_session['sensors']

    async def item_dic(self):
        try:
            response_item_dic = {}
            filter = {"usr_id": self.user.id}
            dynamics_num = await self.dynamics.count_documents(filter)
            dynamic_scenes_num = await self.dynamic_scenes.count_documents(filter)
            environments_num = await self.environments.count_documents(filter)
            sensors_num = await self.sensors.count_documents(filter)

            response_item_dic["dynamic"] = dynamics_num
            response_item_dic["dynamic_scenes"] = dynamic_scenes_num
            response_item_dic["environments"] = environments_num
            response_item_dic["sensors"] = sensors_num

            return response_item_dic
        except:
            raise

