from pydantic.typing import Optional
from pydantic import BaseModel, Field


class CarCreateDTO(BaseModel):
    name: str = Field(..., example="car_1")
    desc: str
    param: dict
    car_snap: dict
    sensors_snap: dict


class CarUpdateDTO(CarCreateDTO):
    ...
