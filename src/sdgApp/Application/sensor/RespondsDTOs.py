from pydantic import BaseModel
from pydantic.typing import List


class SensorReadDTO(BaseModel):
    id: str
    name: str
    type: str
    desc: str
    param: dict
    create_time: str
    last_modified: str


class SensorsResponse(BaseModel):
    total_num: int
    total_page_num: int
    datas: List[SensorReadDTO]