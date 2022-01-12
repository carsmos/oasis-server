from typing import Optional
from pydantic import BaseModel, Field


class AssemberScenarioCreateDTO(BaseModel):
    name: str = Field(..., example="scenario_01")
    desc: Optional[str] = Field(None, example="This is a demo scenario")
    map_name: str = Field(..., example="Town01")
    dynamic_scene_id: str = Field(..., example="e4aKGHrRpM2tBVyVppdYSq")
    env_id: Optional[str] = Field(None, example="e4aKGHrRpM2tBVyVppdYSq")
    env_name: Optional[str] = Field(None, example="ClearNoon")


class AssemberScenarioUpdateDTO(BaseModel):
    name: str = Field(..., example="scenario_01")
    desc: Optional[str] = Field(None, example="This is a demo scenario")
    scenario_param: Optional[dict]



