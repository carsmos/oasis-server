from sdgApp.Domain.dynamic_scenes.scenarios_repo import ScenariosRepo
from sdgApp.Domain.dynamic_scenes.scenarios import ScenariosAggregate


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    pass


class ScenarioRepoImpl(ScenariosRepo):

    def __init__(self, db_session):
        self.db_session = db_session
        self.scenarios_collection = self.db_session['dynamic_scenes']

    def create_scenario(self, scenario: ScenariosAggregate):
        scenario_DO = DataMapper_to_DO(scenario)
        result = self.scenarios_collection.insert_one(scenario_DO)
        return self.scenarios_collection.find_one({"_id": result.inserted_id})

    def delete_scenario_by_id(self, dynamic_scene_id: str):
        result = self.scenarios_collection.delete_one({"dynamic_scene_id": dynamic_scene_id})
        if result.deleted_count != 0:
            return {"status_code": 200, "Detail": "Delete data sucess"}

    def update_scenario(self, dynamic_scene_id: str, scenario: ScenariosAggregate):
        scenario_DO = DataMapper_to_DO(scenario)
        result = self.scenarios_collection.update_one(
            {
                'dynamic_scene_id': dynamic_scene_id,
            }, {'$set': scenario_DO})
        if result.matched_count == 1 and result.modified_count == 1:
            return self.scenarios_collection.find_one({"dynamic_scene_id": dynamic_scene_id})
        else:
            return {"status_code": 400, "Detail": "update data failed"}

    def find_all_scenario(self):
        scenario_list = []
        result = self.scenarios_collection.find()
        for scenario in result:
            scenario_list.append(scenario)
        return scenario_list

    def find_specified_scenario(self, dynamic_scene_id: str):
        result = self.scenarios_collection.find_one({"dynamic_scene_id": dynamic_scene_id})
        return result
