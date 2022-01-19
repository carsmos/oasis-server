from pydantic.typing import Optional
from pydantic import BaseModel, Field


class CarCreateDTO(BaseModel):
    name: str = Field(..., example="car_1")
    desc: Optional[str]
    param: Optional[dict]


class CarUpdateDTO(CarCreateDTO):
    ...

class CarSnapUpdateDTO(BaseModel):
    name: str = Field(..., example="car_1")
    desc: Optional[str]
    param: Optional[dict]
    sensors_snap: Optional[dict]
    car_snap: Optional[dict]