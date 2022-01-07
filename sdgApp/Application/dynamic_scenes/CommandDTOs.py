from datetime import datetime
from typing import Optional, Union, List
from pydantic import BaseModel, Field, validator
from shortuuid import ShortUUID


class ScenarioBaseModel(BaseModel):
    dynamic_scene_id: Optional[str] = Field(None, example="YSuyaz")
    script: str = Field(..., example="This is a demo script")
    scenario_name: str = Field(..., example="scenario_01")
    desc: Optional[str] = Field(None, example="This is a demo script")
    tags: Optional[List[str]] = Field([], example=['tag1', 'tag2'])
    create_time: Union[datetime, str] = datetime.now().strftime("%Y年%m月%d日")
    language: Optional[str] = Field("cartel", example="cartel")

    @validator("dynamic_scene_id", pre=True, always=True)
    def default_id(cls, v):
        return v or ShortUUID().random(6)


class ScenarioCreateDTO(ScenarioBaseModel):
    pass


class ScenarioUpdateDTO(ScenarioBaseModel):
    pass


class ScenarioDeleteDTO(ScenarioBaseModel):
    pass
