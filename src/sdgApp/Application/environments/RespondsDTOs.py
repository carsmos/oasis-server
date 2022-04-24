from pydantic import BaseModel
from pydantic.typing import List
from sdgApp.Application.environments.CommandDTOs import EnvCreateDTO


class EnvReadDTO(EnvCreateDTO):
    id: str
    create_time: str
    last_modified: str


class EnvsResponse(BaseModel):
    total_num: int
    total_page_num: int
    datas: List[EnvReadDTO]