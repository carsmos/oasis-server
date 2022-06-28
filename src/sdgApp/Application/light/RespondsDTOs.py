from pydantic import BaseModel
from pydantic.typing import List
from sdgApp.Application.light.CommandDTOs import LightCreateDTO


class LightReadDTO(LightCreateDTO):
    id: str
    create_time: str
    last_modified: str


class LightResponse(BaseModel):
    total_num: int
    total_page_num: int
    datas: List[LightReadDTO]
