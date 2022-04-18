import shortuuid

from sdgApp.Application.car.usercase import split_page
from sdgApp.Application.scenarios.RespondsDTOs import ScenariosReadDTO
from sdgApp.Application.scenarios.CommandDTOs import ScenarioCreateDTO, ScenarioUpdateDTO
from sdgApp.Domain.scenarios.scenarios import ScenariosAggregate
from sdgApp.Domain.scenarios.scenarios_exceptions import ScenarioNotFoundError
from sdgApp.Infrastructure.MongoDB.scenario.scenario_repoImpl import ScenarioRepoImpl


class ScenarioCommandUsercase(object):

    def __init__(self, db_session, user, repo=ScenarioRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    async def create_scenario(self, scenario_create_model: ScenarioCreateDTO):
        try:
            uuid = shortuuid.uuid()
            scenario = ScenariosAggregate(uuid,
                                          name=scenario_create_model.name,
                                          desc=scenario_create_model.desc,
                                          tags=scenario_create_model.tags,
                                          scenario_param=scenario_create_model.scenario_param
                                          )
            await self.repo.create_scenario(scenario)
        except:
            raise

    async def delete_scenario(self, scenario_id: str):
        try:
            await self.repo.delete_scenario_by_id(scenario_id)
        except:
            raise

    async def update_scenario(self, scenario_id: str, scenario_update_model: ScenarioUpdateDTO):
        try:
            scenario_retrieved = self.repo.get(scenario_id)
            scenario_retrieved.name = scenario_update_model.name
            scenario_retrieved.desc = scenario_update_model.desc
            scenario_retrieved.tags = scenario_update_model.tags
            scenario_retrieved.scenario_param = scenario_update_model.scenario_param
            await self.repo.update_scenario(scenario_id, scenario_retrieved)
        except:
            raise


class ScenarioQueryUsercase(object):

    def __init__(self, db_session, user):
        self.db_session = db_session
        self.scenarios_collection = self.db_session['scenarios']
        self.user = user

    async def find_specified_scenario(self, scenario_id: str):
        try:
            filter = {"id": scenario_id}
            filter.update({"usr_id": self.user.id})
            result_dict = await self.scenarios_collection.find_one(filter)
            if result_dict is None:
                raise ScenarioNotFoundError
            return ScenariosReadDTO(**result_dict)
        except:
            raise

    async def find_all_scenarios(self, p_num):
        try:
            response_dto_list = []
            filter = {}
            filter.update({"usr_id": self.user.id})
            scenario_list = self.scenarios_collection.find(filter).sort([('last_modified', -1)])
            async for scenario in scenario_list:
                response_dto_list.append(ScenariosReadDTO(**scenario))

            response_dto_list = split_page(p_num, response_dto_list)
            return response_dto_list
        except:
            raise
