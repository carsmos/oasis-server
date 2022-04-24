from pydantic import BaseModel
from pydantic.typing import List


class CarReadDTO(BaseModel):
    id: str
    name: str
    desc: str
    param: dict
    sensors_snap: dict
    car_snap: dict
    create_time: str = None
    last_modified: str


class CarsResponse(BaseModel):
    total_num: int
    total_page_num: int
    datas: List[CarReadDTO]