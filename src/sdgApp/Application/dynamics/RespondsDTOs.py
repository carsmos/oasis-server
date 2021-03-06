from pydantic import BaseModel
from pydantic.typing import List


class DynamicsReadDTO(BaseModel):
    id: str
    name: str
    desc: str
    param: dict
    create_time: str
    last_modified: str


class DynamicsResponse(BaseModel):
    total_num: int
    total_page_num: int
    datas: List[DynamicsReadDTO]