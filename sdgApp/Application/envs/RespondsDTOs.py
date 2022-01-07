from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional, Union
from shortuuid import ShortUUID


class EnvReadDTO(BaseModel):
    env_id: Optional[str] = Field(None, example="iDu5rW")
    env_name: str = Field(..., example="env01")
    desc: Optional[str] = Field(None, example="env01")
    create_time: Union[datetime, str] = datetime.now().strftime("%Y年%m月%d日")
    wetness: float = Field(..., example="0")
    cloudiness: float = Field(..., example="0")
    fog_density: float = Field(..., example="0")
    fog_falloff: float = Field(..., example="0")
    fog_distance: float = Field(..., example="0")
    precipitation: float = Field(..., example="0")
    wind_intensity: float = Field(..., example="0")
    sun_azimuth_angle: float = Field(..., example="0")
    sun_altitude_angle: float = Field(..., example="90")
    precipitation_deposits: float = Field(..., example="0")

    @validator("env_id", pre=True, always=True)
    def default_id(cls, v):
        return v or ShortUUID().random(6)
