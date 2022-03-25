from datetime import datetime
from sdgApp.Infrastructure.MongoDB.scenario.scenario_DO import ScenarioDO
from sdgApp.Domain.scenarios.scenarios_repo import ScenariosRepo
from sdgApp.Domain.scenarios.scenarios import ScenariosAggregate
from fastapi import HTTPException


def DataMapper_to_DO(aggregate):
    return aggregate.shortcut_DO


def DataMapper_to_Aggregate(DO):
    pass


class ScenarioRepoImpl(ScenariosRepo):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.user = user
        self.scenarios_collection = self.db_session['scenarios']

    def create_scenario(self, scenario: ScenariosAggregate):
        scenario_DO = ScenarioDO(id=scenario.id,
                                 name=scenario.name,
                                 desc=scenario.desc,
                                 tags=scenario.tags,
                                 usr_id=self.user.id,
                                 scenario_param=scenario.scenario_param,
                                 create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                 last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                 )
        self.scenarios_collection.insert_one(scenario_DO.dict())

    def delete_scenario_by_id(self, scenario_id: str):
        filter = {"id": scenario_id}
        self.scenarios_collection.delete_one(filter)

    def update_scenario(self, scenario_id: str, update_scenario: ScenariosAggregate):
        scenario_DO = ScenarioDO(id=update_scenario.id,
                                 name=update_scenario.name,
                                 desc=update_scenario.desc,
                                 tags=update_scenario.tags,
                                 scenario_param=update_scenario.scenario_param,
                                 usr_id=None,
                                 create_time=None,
                                 last_modified=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                 )
        filter = {'id': scenario_id}
        self.scenarios_collection.update_one(filter, {'$set': scenario_DO.dict(exclude={'usr_id', 'create_time'})})

    def get(self, scenario_id: str):
        filter = {'id': scenario_id}
        result_dict = self.scenarios_collection.find_one(filter, {'_id': 0})
        if result_dict:
            scenario = ScenarioDO(**result_dict).to_entity()
            return scenario

    def list(self):
        filter = {}
        scenario_aggregate_lst = []
        results_dict = self.scenarios_collection.find(filter)
        if results_dict:
            for one_result in results_dict:
                one_scenario = ScenarioDO(**one_result).to_entity()
                scenario_aggregate_lst.append(one_scenario)
            return scenario_aggregate_lst
