from sdgApp.Application.dynamic_scenes.usercase import DynamicSceneQueryUsercase
from sdgApp.Application.weather.usercase import WeatherQueryUsercase
from sdgApp.Application.scenarios.usercase import ScenarioCommandUsercase
from sdgApp.Application.ScenariosFacadeService.CommandDTOs import AssemberScenarioCreateDTO
from sdgApp.Application.scenarios.CommandDTOs import ScenarioCreateDTO, ScenarioUpdateDTO
from sdgApp.Application.light.usercase import LightQueryUsercase


async def AssembleScenarioService(scenario_create_model: AssemberScenarioCreateDTO, db, user):
    dynamic_scene = await DynamicSceneQueryUsercase(
        db_session=db, user=user).find_specified_scenario(scenario_create_model.dynamic_scene_id)

    weather = await WeatherQueryUsercase(
        db_session=db, user=user).find_specified_weather(scenario_create_model.weather_id)
    light = await LightQueryUsercase(db_session=db, user=user).find_specified_light(scenario_create_model.light_id)
    weather_parma = dict(weather.dict().get("param"), **light.dict().get("param"))
    scenario_param = {"map_name": scenario_create_model.map_name, "dynamic_scene": dynamic_scene,
                      "environment": weather_parma, "evaluation_standard": scenario_create_model.evaluation_standard,
                      "traffic_flow": scenario_create_model.traffic_flow}
    if not scenario_create_model.id:
        scenario_create_model = ScenarioCreateDTO(name=scenario_create_model.name,
                                                  desc=scenario_create_model.desc,
                                                  tags=scenario_create_model.tags,
                                                  scenario_param=scenario_param,
                                                  )
        return await ScenarioCommandUsercase(db, user).create_scenario(scenario_create_model)
    else:
        scenario_update_model = ScenarioUpdateDTO(name=scenario_create_model.name,
                                                  desc=scenario_create_model.desc,
                                                  tags=scenario_create_model.tags,
                                                  scenario_param=scenario_param
                                                  )
        return await ScenarioCommandUsercase(db, user).update_scenario(scenario_create_model.id, scenario_update_model)