from datetime import datetime

from sdgApp.Domain.scenarios.scenarios_repo import ScenariosRepo
from sdgApp.Domain.scenarios.scenarios import ScenariosAggregate
from fastapi import HTTPException


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    pass


class ScenarioRepoImpl(ScenariosRepo):

    def __init__(self, db_session):
        self.db_session = db_session
        self.scenarios_collection = self.db_session['scenarios']

    def create_scenario(self, scenario: ScenariosAggregate):
        scenario_DO = {"id": scenario.id,
                       "name": scenario.name,
                       "desc": scenario.desc,
                       "scenario_param": scenario.scenario_param}
        scenario_DO.update({"create_time": datetime.now(),
                            "last_modified": None})
        result = self.scenarios_collection.insert_one(scenario_DO)
        if result:
            return scenario.id

    def delete_scenario_by_id(self, scenario_id: str):
        result = self.scenarios_collection.delete_one({"id": scenario_id})
        if result.deleted_count != 0:
            return {"status_code": 200, "Detail": "Delete data sucess"}

    def update_scenario(self, scenario_id: str, scenario: ScenariosAggregate):
        scenario_DO = {"name": scenario.name,
                       "desc": scenario.desc,
                       "scenario_param": scenario.scenario_param}
        scenario_DO.update({"last_modified": datetime.now()})
        result = self.scenarios_collection.update_one(
            {
                'id': scenario_id,
            }, {'$set': scenario_DO})
        if result.matched_count == 1 and result.modified_count == 1:
            return True
        else:
            raise HTTPException(status_code=400, detail="update data failed")

    def find_all_scenario(self):
        scenario_aggregate_list = []
        results_DO = self.scenarios_collection.find({}, {'_id': 0})
        if results_DO:
            for one_result in results_DO:
                one_scenario = ScenariosAggregate(id=one_result["id"])
                one_scenario.save_DO_shortcut(one_result)
                scenario_aggregate_list.append(one_scenario)
            return scenario_aggregate_list

    def find_specified_scenario(self, scenario_id: str):
        result_DO = self.scenarios_collection.find_one({"id": scenario_id}, {'_id': 0})
        if result_DO:
            scenario = ScenariosAggregate(result_DO["id"])
            scenario.save_DO_shortcut(result_DO)
            return scenario
