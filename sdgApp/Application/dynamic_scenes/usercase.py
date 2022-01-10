from sdgApp.Application.dynamic_scenes.RespondsDTOs import ScenarioReadDTO
from sdgApp.Application.dynamic_scenes.CommandDTOs import ScenarioCreateDTO, ScenarioUpdateDTO
from sdgApp.Domain.dynamic_scenes.dynamic_scenes import ScenariosAggregate
from sdgApp.Infrastructure.MongoDB.dynamic_scene.dynamic_scene_repoImpl import ScenarioRepoImpl
from sdgApp.Infrastructure.MongoDB.session_maker import mongo_session


def DTO_assembler(scenario: ScenariosAggregate):
    return scenario.shortcut_DO


class ScenarioCommandUsercase(object):

    def __init__(self, db_session, repo=ScenarioRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session)

    def create_scenario(self, dto: ScenarioCreateDTO):
        try:
            scenario_dict = dto.dict()
            scenario = ScenariosAggregate(
                dynamic_scene_id=scenario_dict["dynamic_scene_id"],
                script=scenario_dict["script"],
                dynamic_scene_name=scenario_dict["dynamic_scene_name"],
                desc=scenario_dict["desc"],
                create_time=scenario_dict["create_time"],)
            scenario.save_DO_shortcut(scenario_dict)
            return self.repo.create_scenario(scenario)
        except:
            raise


class ScenarioDeleteUsercase(object):

    def __init__(self, db_session, repo=ScenarioRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session)

    def delete_scenario(self, dynamic_scene_id: str):
        try:
            return self.repo.delete_scenario_by_id(dynamic_scene_id)
        except:
            raise


class ScenarioUpdateUsercase(object):

    def __init__(self, db_session, repo=ScenarioRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session)

    def update_scenario(self, dynamic_scene_id: str, dto: ScenarioUpdateDTO):
        try:
            scenario_dict = dto.dict()
            scenario = ScenariosAggregate(
                dynamic_scene_id=scenario_dict["dynamic_scene_id"],
                script=scenario_dict["script"],
                dynamic_scene_name=scenario_dict["dynamic_scene_name"],
                desc=scenario_dict["desc"],
                create_time=scenario_dict["create_time"],
            )
            scenario.save_DO_shortcut(scenario_dict)
            return self.repo.update_scenario(dynamic_scene_id, scenario)
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
                response_dto = DTO_assembler(scenario)
                response_dto_list.append(response_dto)
            return response_dto_list
        except:
            raise

    def find_specified_scenario(self, dynamic_scene_id: str):
        try:
            scenario = self.repo.find_specified_scenario(dynamic_scene_id)
            response_dto = DTO_assembler(scenario)
            return response_dto
        except:
            raise
