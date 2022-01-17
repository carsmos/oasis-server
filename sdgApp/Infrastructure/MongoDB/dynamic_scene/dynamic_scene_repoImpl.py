from datetime import datetime

from sdgApp.Domain.dynamic_scenes.dynamic_scenes_repo import DynamicScenesRepo
from sdgApp.Domain.dynamic_scenes.dynamic_scenes import DynamicScenesAggregate
from fastapi import HTTPException


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
        scenario_DO = {"id": scenario.id,
                       "name": scenario.name,
                       "desc": scenario.desc,
                       "scene_script": scenario.scene_script}
        scenario_DO.update({"create_time": datetime.now(),
                            "last_modified": None})
        result = self.scenarios_collection.insert_one(scenario_DO)
        if result.inserted_id:
            return scenario.id

    def delete_scenario_by_id(self, dynamic_scene_id: str):
        result = self.scenarios_collection.delete_one({"id": dynamic_scene_id})
        if result.deleted_count != 0:
            return {"status_code": 200, "Detail": "Delete data sucess"}

    def update_scenario(self, dynamic_scene_id: str, scenario: DynamicScenesAggregate):
        scenario_DO = {"name": scenario.name,
                       "desc": scenario.desc,
                       "scene_script": scenario.scene_script}
        scenario_DO.update({"last_modified": datetime.now()})
        result = self.scenarios_collection.update_one(
            {
                'id': dynamic_scene_id,
            }, {'$set': scenario_DO})
        if result.matched_count == 1 and result.modified_count == 1:
            return True
        else:
            raise HTTPException(status_code=400, detail="data update failed")

    def find_all_scenario(self):
        scnenario_aggregate_list = []
        results_DO = self.scenarios_collection.find({}, {'_id': 0})
        if results_DO:
            for one_result in results_DO:
                one_scene = DynamicScenesAggregate(one_result["id"])
                one_scene.save_DO_shortcut(one_result)
                scnenario_aggregate_list.append(one_scene)
            return scnenario_aggregate_list

    def find_specified_scenario(self, dynamic_scene_id: str):
        result_DO = self.scenarios_collection.find_one({"id": dynamic_scene_id},
                                                       {'_id': 0})
        if result_DO:
            scenario = DynamicScenesAggregate(result_DO["id"])
            scenario.save_DO_shortcut(result_DO)
            return scenario
