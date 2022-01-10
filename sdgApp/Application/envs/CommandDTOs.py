from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field, validator
from shortuuid import ShortUUID


class EnvBaseModel(BaseModel):
    env_id: Optional[str] = Field(None, example="iDu5rW")
    env_name: str = Field(..., example="env01")
    desc: Optional[str] = Field(None, example="env01")
    create_time: Union[datetime, str] = datetime.now().strftime("%Y年%m月%d日")
    param: Optional[dict]

    @validator("env_id", pre=True, always=True)
    def default_id(cls, v):
        return v or ShortUUID().random(6)


class EnvCreateDTO(EnvBaseModel):
    pass


class EnvUpdateDTO(EnvBaseModel):
    pass


class EnvDeleteDTO(EnvBaseModel):
    pass
