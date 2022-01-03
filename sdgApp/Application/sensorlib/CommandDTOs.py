from pydantic.typing import Optional
from pydantic import BaseModel, Field


class SensorBase(BaseModel):
    name: str
    desc: Optional[str]
    type: str = Field(example="RGB_camera")
    param: str


class SensorCreateDTO(SensorBase):
    ...

class SensorUpdateDTO(SensorBase):
    id: str

class SensorDeleteDTO(BaseModel):
    id: str



