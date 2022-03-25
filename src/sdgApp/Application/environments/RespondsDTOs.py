from datetime import datetime
from typing import Union
from sdgApp.Application.environments.CommandDTOs import EnvCreateDTO


class EnvReadDTO(EnvCreateDTO):
    id: str
    create_time: str
    last_modified: str
