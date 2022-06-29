from typing import Optional
from pydantic import BaseModel, Field


class ScenarioCreateDTO(BaseModel):
    name: str = Field(..., example="scenario_01")
    desc: Optional[str] = Field(None, example="This is a demo scenario")
    scenario_param: Optional[dict]
    tags: Optional[list] = Field([], example=['tag1', 'tag2'])


class ScenarioUpdateDTO(ScenarioCreateDTO):
    pass


