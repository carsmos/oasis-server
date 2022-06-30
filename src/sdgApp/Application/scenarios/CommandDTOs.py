from typing import Optional, Any
from pydantic import BaseModel, Field


class ScenarioCreateDTO(BaseModel):
    name: str = Field(..., example="scenario_01")
    desc: Optional[str] = Field(None, example="This is a demo scenario")
    scenario_param: Optional[dict]
    tags: Optional[list] = Field([], example=['tag1', 'tag2'])
    types: str = Field(..., example="file")
    parent_id: Any = Field(..., example="root")

class ScenarioUpdateDTO(ScenarioCreateDTO):
    pass


class TrafficFLowBlueprintDTO(BaseModel):
    id: str
    actor: str
    actor_class: str
    check: bool = True
