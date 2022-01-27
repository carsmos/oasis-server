from datetime import datetime
from typing import Union
from sdgApp.Application.scenarios.CommandDTOs import ScenarioCreateDTO


class ScenariosReadDTO(ScenarioCreateDTO):
   id: str
   create_time: datetime
   last_modified: Union[None, datetime]