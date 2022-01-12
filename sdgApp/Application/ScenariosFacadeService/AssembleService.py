from sdgApp.Application.dynamic_scenes.usercase import DynamicSceneQueryUsercase
from sdgApp.Application.environments.usercase import EnvQueryUsercase
from sdgApp.Application.scenarios.usercase import ScenarioCommandUsercase


def AssembleScenarioService(scenario_create_model: dict, db):
    scenario_dto = scenario_create_model
    dynamic_scene = DynamicSceneQueryUsercase(
        db_session=db).find_specified_scenario(scenario_dto["dynamic_scene_id"])
    environment = ""
    if scenario_dto["env_id"]:
        environment = EnvQueryUsercase(
            db_session=db).find_specified_env(scenario_dto["env_id"])
    if scenario_dto["env_name"]:
        environment = scenario_dto["env_name"]
    scenario_dto.update({"scenario_param": {}})
    scenario_dto["scenario_param"]["map_name"] = scenario_dto["map_name"]
    scenario_dto["scenario_param"]["dynamic_scene"] = dynamic_scene
    scenario_dto["scenario_param"]["environment"] = environment
    return ScenarioCommandUsercase(db).create_scenario(scenario_dto)






