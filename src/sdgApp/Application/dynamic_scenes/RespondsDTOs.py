from sdgApp.Application.dynamic_scenes.CommandDTOs import DynamicSceneCreateDTO
from pydantic import BaseModel
from pydantic.typing import List


class DynamicSceneReadDTO(DynamicSceneCreateDTO):
    id: str
    create_time: str
    last_modified: str


class DynamicScenesResponse(BaseModel):
    total_num: str
    total_page_num: str
    datas: List[DynamicSceneReadDTO]