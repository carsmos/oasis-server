import shortuuid
from sdgApp.Application.scenarios.RespondsDTOs import ScenariosReadDTO
from sdgApp.Application.scenarios.CommandDTOs import ScenarioCreateDTO, ScenarioUpdateDTO
from sdgApp.Domain.scenarios.scenarios import ScenariosAggregate
from sdgApp.Infrastructure.MongoDB.scenario.scenario_repoImpl import ScenarioRepoImpl


def dto_assembler(scenario: ScenariosAggregate):
    return scenario.shortcut_DO


class ScenarioCommandUsercase(object):

    def __init__(self, db_session, user, repo=ScenarioRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def create_scenario(self, scenario_create_model: ScenarioCreateDTO):
        try:
            uuid = shortuuid.uuid()
            scenario = ScenariosAggregate(uuid,
                                          name=scenario_create_model.name,
                                          desc=scenario_create_model.desc,
                                          tags=scenario_create_model.tags,
                                          scenario_param=scenario_create_model.scenario_param
                                          )
            self.repo.create_scenario(scenario)
        except:
            raise

    def delete_scenario(self, scenario_id: str):
        try:
            self.repo.delete_scenario_by_id(scenario_id)
        except:
            raise

    def update_scenario(self, scenario_id: str, scenario_update_model: ScenarioCreateDTO):
        try:
            scenario_retrieved = self.repo.get(scenario_id)
            scenario_retrieved.name = scenario_update_model.name
            scenario_retrieved.desc = scenario_update_model.desc
            scenario_retrieved.tags = scenario_update_model.tags
            scenario_retrieved.scenario_param = scenario_update_model.scenario_param
            self.repo.update_scenario(scenario_id, scenario_retrieved)
        except:
            raise


class ScenarioQueryUsercase(object):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.scenarios_collection = self.db_session['scenarios']
        self.user = user

    def find_specified_scenario(self, scenario_id: str):
        try:
            filter = {"id": scenario_id}
            result_dict = self.scenarios_collection.find_one(filter)
            return ScenariosReadDTO(**result_dict)
        except:
            raise

    def find_all_scenarios(self):
        try:
            response_dto_list = []
            filter = {}
            scenario_list = self.scenarios_collection.find(filter)
            for scenario in scenario_list:
                response_dto_list.append(ScenariosReadDTO(**scenario))
            return response_dto_list
        except:
            raise
