from typing import Optional
from pydantic import BaseModel, Field


class DynamicSceneCreateDTO(BaseModel):
    name: str = Field(..., example="scenario_01")
    desc: Optional[str] = Field(None, example="This is a demo script")
    param: Optional[dict]


class DynamicSceneUpdateDTO(DynamicSceneCreateDTO):
    pass
