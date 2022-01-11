from sdgApp.Application.dynamic_scenes.CommandDTOs import DynamicSceneCreateDTO
from datetime import datetime
from typing import Union


class DynamicSceneReadDTO(DynamicSceneCreateDTO):
    id: str
    create_time: datetime
    last_modified: Union[None, datetime]
