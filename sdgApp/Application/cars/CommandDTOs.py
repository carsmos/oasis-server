from pydantic.typing import Optional, List
from pydantic import BaseModel, Field


class CarCreateDTO(BaseModel):
    name: str = Field(..., example="car_1")
    desc: Optional[str]
    param: Optional[dict]

class CarUpdateDTO(CarCreateDTO):
    ...