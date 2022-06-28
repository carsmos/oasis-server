from sdgApp.Application.dynamic_scenes.usercase import DynamicSceneQueryUsercase
from sdgApp.Application.weather.usercase import WeatherQueryUsercase
from sdgApp.Application.scenarios.usercase import ScenarioCommandUsercase
from sdgApp.Application.ScenariosFacadeService.CommandDTOs import AssemberScenarioCreateDTO
from sdgApp.Application.scenarios.CommandDTOs import ScenarioCreateDTO, ScenarioUpdateDTO


async def AssembleScenarioService(scenario_create_model: AssemberScenarioCreateDTO, db, user):
    dynamic_scene = await DynamicSceneQueryUsercase(
        db_session=db, user=user).find_specified_scenario(scenario_create_model.dynamic_scene_id)
    environments = ["ClearNoon", "CloudyNoon", "WetNoon", "WetCloudyNoon", "SoftRainNoon",
                    "MidRainyNoon", "HardRainNoon", "ClearSunset", "CloudySunset", "WetSunset",
                    "WetCloudySunset", "SoftRainSunset", "MidRainSunset", "HardRainSunset"]
    if scenario_create_model.weather_id in environments:
        environment = {"param": scenario_create_model.weather_id}
    else:
        environment = await WeatherQueryUsercase(
            db_session=db, user=user).find_specified_weather(scenario_create_model.weather_id)
    scenario_param = {"map_name": scenario_create_model.map_name, "dynamic_scene": dynamic_scene,
                      "weather": environment}
    if not scenario_create_model.id:
        scenario_create_model = ScenarioCreateDTO(name=scenario_create_model.name,
                                                  desc=scenario_create_model.desc,
                                                  tags=scenario_create_model.tags,
                                                  scenario_param=scenario_param)
        return await ScenarioCommandUsercase(db, user).create_scenario(scenario_create_model)
    else:
        scenario_update_model = ScenarioUpdateDTO(name=scenario_create_model.name,
                                                  desc=scenario_create_model.desc,
                                                  tags=scenario_create_model.tags,
                                                  scenario_param=scenario_param)
        return await ScenarioCommandUsercase(db, user).update_scenario(scenario_create_model.id, scenario_update_model)