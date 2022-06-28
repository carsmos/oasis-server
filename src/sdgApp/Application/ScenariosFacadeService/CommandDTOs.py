from typing import Optional
from pydantic import BaseModel, Field


class AssemberScenarioCreateDTO(BaseModel):
    id: Optional[str]
    name: str = Field(..., example="scenario_01")
    desc: Optional[str] = Field(None, example="This is a demo scenario")
    map_name: str = Field(..., example="Town01")
    dynamic_scene_id: str = Field(..., example="e4aKGHrRpM2tBVyVppdYSq")
    weather_id: str = Field(None, example="e4aKGHrRpM2tBVyVppdYSq or CloudyNoon")
    tags: Optional[list] = Field([], example=['tag1', 'tag2'])




