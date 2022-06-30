from pydantic import BaseModel
from pydantic.typing import Any

from sdgApp.Application.scenarios.CommandDTOs import TrafficFLowBlueprintDTO
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
    types: str
    parent_id: Any

    def to_entity(self) -> ScenariosAggregate:
        return ScenariosAggregate(
            id=self.id,
            name=self.name,
            desc=self.desc,
            tags=self.tags,
            types= self.types,
            parent_id= self.parent_id,
            scenario_param=self.scenario_param
        )

class TrafficFLowBlueprintDO(BaseModel):
    id: str
    actor: str
    actor_class: str
    create_time: str = None
    last_modified: str = None

    def to_entity(self) -> TrafficFLowBlueprintDTO:
        return TrafficFLowBlueprintDTO(
            id=self.id,
            actor=self.actor,
            actor_class=self.actor_class
        )
