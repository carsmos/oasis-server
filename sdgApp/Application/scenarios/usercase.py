import shortuuid

from sdgApp.Application.scenarios.CommandDTOs import ScenarioCreateDTO, ScenarioUpdateDTO
from sdgApp.Domain.scenarios.scenarios import ScenariosAggregate
from sdgApp.Infrastructure.MongoDB.scenario.scenario_repoImpl import ScenarioRepoImpl


def dto_assembler(scenario: ScenariosAggregate):
    return scenario.shortcut_DO


class ScenarioCommandUsercase(object):

    def __init__(self, db_session, repo=ScenarioRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session)

    def create_scenario(self, dto: dict):
        try:
            uuid = shortuuid.uuid()
            scenario_dict = dto
            scenario = ScenariosAggregate(uuid,
                                          name=scenario_dict["name"],
                                          desc=scenario_dict["desc"],
                                          tags=scenario_dict["tags"],
                                          scenario_param=scenario_dict["scenario_param"]
                                          )
            return self.repo.create_scenario(scenario)
        except:
            raise

    def delete_scenario(self, scenario_id: str):
        try:
            return self.repo.delete_scenario_by_id(scenario_id)
        except:
            raise

    def update_scenario(self, scenario_id: str, dto: dict):
        try:
            scenario_dict = dto
            scenario = ScenariosAggregate(
                scenario_id,
                name=scenario_dict["name"],
                desc=scenario_dict["desc"],
                tags=scenario_dict["tags"],
                scenario_param=scenario_dict["scenario_param"]
            )
            return self.repo.update_scenario(scenario_id, scenario)
        except:
            raise


class ScenarioQueryUsercase(object):

    def __init__(self, db_session, repo=ScenarioRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session)

    def find_all_scenarios(self):
        try:
            response_dto_list = []
            scenario_list = self.repo.find_all_scenario()
            for scenario in scenario_list:
                response_dto = dto_assembler(scenario)
                response_dto_list.append(response_dto)
            return response_dto_list
        except:
            raise

    def find_specified_scenario(self, scenario_id: str):
        try:
            result = self.repo.find_specified_scenario(scenario_id)
            response_dto = dto_assembler(result)
            return response_dto
        except:
            raise
