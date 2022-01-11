from datetime import datetime

from sdgApp.Domain.dynamic_scenes.dynamic_scenes_repo import ScenariosRepo
from sdgApp.Domain.dynamic_scenes.dynamic_scenes import ScenariosAggregate
from fastapi import HTTPException


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    pass


class ScenarioRepoImpl(ScenariosRepo):

    def __init__(self, db_session):
        self.db_session = db_session
        self.scenarios_collection = self.db_session['dynamic_scenes']

    def create_scenario(self, scenario: ScenariosAggregate):
        scenario_DO = {"id": scenario.id,
                       "name": scenario.name,
                       "desc": scenario.desc,
                       "param": scenario.param}
        scenario_DO.update({"create_time": datetime.now(),
                            "last_modified": None})
        result = self.scenarios_collection.insert_one(scenario_DO)
        if result:
            return scenario.id

    def delete_scenario_by_id(self, dynamic_scene_id: str):
        result = self.scenarios_collection.delete_one({"id": dynamic_scene_id})
        if result.deleted_count != 0:
            return {"status_code": 200, "Detail": "Delete data sucess"}

    def update_scenario(self, dynamic_scene_id: str, scenario: ScenariosAggregate):
        scenario_DO = {"name": scenario.name,
                       "desc": scenario.desc,
                       "param": scenario.param}
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
        for one_result in results_DO:
            one_scene = ScenariosAggregate(one_result["id"])
            one_scene.save_DO_shortcut(one_result)
            scnenario_aggregate_list.append(one_scene)
        return scnenario_aggregate_list

    def find_specified_scenario(self, dynamic_scene_id: str):
        result_DO = self.scenarios_collection.find_one({"id": dynamic_scene_id},
                                                       {'_id': 0})
        scenario = ScenariosAggregate(result_DO["id"])
        scenario.save_DO_shortcut(result_DO)
        return scenario
