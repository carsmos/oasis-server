from typing import Optional, List
from pydantic import BaseModel, Field

from sdgApp.Application.ScenariosFacadeService.CommandDTOs import EvaluationStandard, TrafficFlow


class ScenarioCreateDTO(BaseModel):
    name: str = Field(..., example="scenario_01")
    desc: Optional[str] = Field(None, example="This is a demo scenario")
    scenario_param: Optional[dict]
    tags: Optional[list] = Field([], example=['tag1', 'tag2'])
    evaluation_standard: Optional[EvaluationStandard]
    traffic_flow: Optional[List[TrafficFlow]]


class ScenarioUpdateDTO(ScenarioCreateDTO):
    pass


class TrafficFLowBlueprintDTO(BaseModel):
    id: str
    actor: str
    actor_class: str
