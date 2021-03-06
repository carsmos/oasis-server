from datetime import datetime
from typing import Union
from sdgApp.Application.scenarios.CommandDTOs import ScenarioCreateDTO
from pydantic import BaseModel
from pydantic.typing import List


class ScenariosReadDTO(ScenarioCreateDTO):
   id: str
   create_time: datetime
   last_modified: Union[None, datetime]


class ScenariosResponse(BaseModel):
   total_num: int
   total_page_num: int
   datas: List[ScenariosReadDTO]