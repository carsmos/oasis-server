import shortuuid

from sdgApp.Application.dynamic_scenes.CommandDTOs import DynamicSceneCreateDTO, DynamicSceneUpdateDTO
from sdgApp.Domain.dynamic_scenes.dynamic_scenes import DynamicScenesAggregate
from sdgApp.Infrastructure.MongoDB.dynamic_scene.dynamic_scene_repoImpl import DynamicSceneRepoImpl


def dto_assembler(scenario: DynamicScenesAggregate):
    return scenario.shortcut_DO


class DynamicSceneCommandUsercase(object):

    def __init__(self, db_session, repo=DynamicSceneRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session)

    def create_scenario(self, dto: dict):
        try:
            uuid = shortuuid.uuid()
            scenario_dict = dto
            scenario = DynamicScenesAggregate(
                uuid,
                name=scenario_dict["name"],
                desc=scenario_dict["desc"],
                scene_script=scenario_dict["scene_script"])
            return self.repo.create_scenario(scenario)
        except:
            raise

    def delete_scenario(self, dynamic_scene_id: str):
        try:
            return self.repo.delete_scenario_by_id(dynamic_scene_id)
        except:
            raise

    def update_scenario(self, dynamic_scene_id: str, dto: dict):
        try:
            scenario_dict = dto
            scenario = DynamicScenesAggregate(
                dynamic_scene_id,
                name=scenario_dict["name"],
                desc=scenario_dict["desc"],
                scene_script=scenario_dict["scene_script"]
            )
            return self.repo.update_scenario(dynamic_scene_id, scenario)
        except:
            raise


class DynamicSceneQueryUsercase(object):

    def __init__(self, db_session, repo=DynamicSceneRepoImpl):
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

    def find_specified_scenario(self, dynamic_scene_id: str):
        try:
            scenario = self.repo.find_specified_scenario(dynamic_scene_id)
            response_dto = dto_assembler(scenario)
            return response_dto
        except:
            raise
