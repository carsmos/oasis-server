from datetime import datetime
from typing import Union
from sdgApp.Application.environments.CommandDTOs import EnvCreateDTO


class EnvReadDTO(EnvCreateDTO):
    id: str
    create_time: datetime
    last_modified: Union[None, datetime]
