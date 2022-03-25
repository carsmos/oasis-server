from pydantic import BaseModel
from pydantic.typing import Any
from sdgApp.Domain.scenarios.scenarios import ScenariosAggregate


class ScenarioDO(BaseModel):
    id: str
    name: str
    desc: str
    scenario_param: dict
    usr_id: Any
    tags: Any
    create_time: str = None
    last_modified: str

    def to_entity(self) -> ScenariosAggregate:
        return ScenariosAggregate(
            id=self.id,
            name=self.name,
            desc=self.desc,
            tags=self.tags,
            scenario_param=self.scenario_param
        )