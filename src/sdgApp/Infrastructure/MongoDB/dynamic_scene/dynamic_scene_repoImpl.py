from datetime import datetime
from sdgApp.Infrastructure.MongoDB.dynamic_scene.dynamic_scene_DO import DynamicSceneDO
from sdgApp.Domain.dynamic_scenes.dynamic_scenes_repo import DynamicScenesRepo
from sdgApp.Domain.dynamic_scenes.dynamic_scenes import DynamicScenesAggregate


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    pass


class DynamicSceneRepoImpl(DynamicScenesRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.scenarios_collection = self.db_session['dynamic_scenes']

    def create_scenario(self, scenario: DynamicScenesAggregate):
        scenario_DO = DynamicSceneDO(id=scenario.id,
                                     name=scenario.name,
                                     desc=scenario.desc,
                                     scene_script=scenario.scene_script,
                                     type=scenario.type,
                                     usr_id=self.user.id,
                                     create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                     last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                     )
        self.scenarios_collection.insert_one(scenario_DO.dict())

    def delete_scenario_by_id(self, dynamic_scene_id: str):
        filter = {"id": dynamic_scene_id}
        filter.update({"usr_id": self.user.id})
        self.scenarios_collection.delete_one(filter)

    def update_scenario(self, dynamic_scene_id: str, update_scenario: DynamicScenesAggregate):
        update_scenario_DO = DynamicSceneDO(id=update_scenario.id,
                                            name=update_scenario.name,
                                            desc=update_scenario.desc,
                                            scene_script=update_scenario.scene_script,
                                            type=update_scenario.type,
                                            create_time=None,
                                            usr_id=None,
                                            last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        filter = {'id': dynamic_scene_id}
        filter.update({"usr_id": self.user.id})
        self.scenarios_collection.update_one(filter,
                                             {'$set': update_scenario_DO.dict(exclude={'create_time','usr_id'})})

    def get(self, dynamic_scene_id: str):
        filter = {'id': dynamic_scene_id}
        filter.update({"usr_id": self.user.id})
        result_dict = self.scenarios_collection.find_one(filter, {'_id': 0})
        if result_dict:
            scenario = DynamicSceneDO(**result_dict).to_entity()
            return scenario

    def list(self):
        filter = {"usr_id": self.user.id}
        filter.update({"usr_id": self.user.id})
        scenario_aggregate_lst = []
        results_dict = self.scenarios_collection.find(filter, {'_id': 0})
        if results_dict:
            for one_result in results_dict:
                one_scenario = DynamicSceneDO(**one_result).to_entity()
                scenario_aggregate_lst.append(one_scenario)
            return scenario_aggregate_lst
