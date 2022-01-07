from sdgApp.Application.dynamic_scenes.RespondsDTOs import ScenarioReadDTO
from sdgApp.Application.dynamic_scenes.CommandDTOs import ScenarioCreateDTO, ScenarioUpdateDTO
from sdgApp.Domain.dynamic_scenes.scenarios import ScenariosAggregate
from sdgApp.Infrastructure.MongoDB.dynamic_scene.scenario_repoImpl import ScenarioRepoImpl
from sdgApp.Infrastructure.MongoDB.session_maker import mongo_session


class ScenarioCommandUsercase(object):

    def __init__(self, repo=ScenarioRepoImpl, db_session=mongo_session):
        self.repo = repo
        _, db = db_session()
        self.repo = self.repo(db)

    def create_scenario(self, dto: ScenarioCreateDTO):
        try:
            scenario_dict = dto.dict()
            scenario = ScenariosAggregate(
                dynamic_scene_id=scenario_dict["dynamic_scene_id"],
                script=scenario_dict["script"],
                scenario_name=scenario_dict["scenario_name"],
                desc=scenario_dict["desc"],
                tags=["tags"],
                create_time=scenario_dict["create_time"],
                language=scenario_dict["language"])
            scenario.save_DO_shortcut(scenario_dict)
            return self.repo.create_scenario(scenario)
        except:
            raise


class ScenarioDeleteUsercase(object):

    def __init__(self, repo=ScenarioRepoImpl, db_session=mongo_session):
        self.repo = repo
        _, db = db_session()
        self.repo = self.repo(db)

    def delete_scenario(self, dynamic_scene_id: str):
        try:
            return self.repo.delete_scenario_by_id(dynamic_scene_id)
        except:
            raise


class ScenarioUpdateUsercase(object):

    def __init__(self, repo=ScenarioRepoImpl, db_session=mongo_session):
        self.repo = repo
        _, db = db_session()
        self.repo = self.repo(db)

    def update_scenario(self, dynamic_scene_id: str, dto: ScenarioUpdateDTO):
        try:
            scenario_dict = dto.dict()
            scenario = ScenariosAggregate(
                dynamic_scene_id=scenario_dict["dynamic_scene_id"],
                script=scenario_dict["script"],
                scenario_name=scenario_dict["scenario_name"],
                desc=scenario_dict["desc"],
                tags=["tags"],
                create_time=scenario_dict["create_time"],
                language=scenario_dict["language"]
            )
            scenario.save_DO_shortcut(scenario_dict)
            return self.repo.update_scenario(dynamic_scene_id, scenario)
        except:
            raise


class ScenarioQueryUsercase(object):

    def __init__(self, repo=ScenarioRepoImpl, db_session=mongo_session):
        self.repo = repo
        _, db = db_session()
        self.repo = self.repo(db)

    def find_all_scenarios(self):
        try:
            return self.repo.find_all_scenario()
        except:
            raise

    def find_specified_scenario(self, dynamic_scene_id: str):
        try:
            return self.repo.find_specified_scenario(dynamic_scene_id)
        except:
            raise
