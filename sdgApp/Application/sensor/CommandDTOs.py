from pydantic.typing import Optional
from pydantic import BaseModel, Field


class SensorCreateDTO(BaseModel):
    name: str = Field(..., example="RGB Camera")
    type: str = Field(..., example="sensor.camera.rgb")
    car_name: str = Field(..., example="car_1")
    car_id: str = Field(..., example="1234")
    desc: Optional[str]
    param: Optional[dict]


class SensorUpdateDTO(SensorCreateDTO):
    ...




