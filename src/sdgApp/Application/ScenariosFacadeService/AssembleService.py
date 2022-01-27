from sdgApp.Application.dynamic_scenes.usercase import DynamicSceneQueryUsercase
from sdgApp.Application.environments.usercase import EnvQueryUsercase
from sdgApp.Application.scenarios.usercase import ScenarioCommandUsercase


def AssembleScenarioService(scenario_create_model: dict, db, user):
    scenario_dto = scenario_create_model
    dynamic_scene = DynamicSceneQueryUsercase(
        db_session=db, user=user).find_specified_scenario(scenario_dto["dynamic_scene_id"])
    environments = ["ClearNoon", "CloudyNoon", "WetNoon", "WetCloudyNoon", "SoftRainNoon",
                    "MidRainyNoon", "HardRainNoon", "ClearSunset", "CloudySunset", "WetSunset",
                    "WetCloudySunset", "SoftRainSunset", "MidRainSunset", "HardRainSunset"]
    if scenario_dto["env_id"] in environments:
        environment = {"weather_param": scenario_dto["env_id"]}
    else:
        environment = EnvQueryUsercase(
            db_session=db, user=user).find_specified_env(scenario_dto["env_id"])
    scenario_dto.update({"scenario_param": {}})
    scenario_dto["scenario_param"]["map_name"] = scenario_dto["map_name"]
    scenario_dto["scenario_param"]["dynamic_scene"] = dynamic_scene
    scenario_dto["scenario_param"]["environment"] = environment
    return ScenarioCommandUsercase(db, user).create_scenario(scenario_dto)






