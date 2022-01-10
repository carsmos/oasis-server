from pydantic.typing import Optional
from pydantic import BaseModel, Field


class WheelCreateDTO(BaseModel):
    name: str = Field(..., example="Wheels_1")
    car_name: str = Field(..., example="car_1")
    car_id: str = Field(..., example="1234")
    desc: Optional[str]
    param: Optional[dict]


class WheelUpdateDTO(WheelCreateDTO):
    ...




