from typing import Optional
from pydantic import BaseModel, Field


class ScenarioCreateDTO(BaseModel):
    name: str = Field(..., example="scenario_01")
    desc: Optional[str] = Field(None, example="This is a demo scenario")
    param: Optional[dict]


class ScenarioUpdateDTO(ScenarioCreateDTO):
    pass


