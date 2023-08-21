from typing import List

from pydantic import BaseModel
from pydantic.typing import Optional


class CreateJob(BaseModel):
    name: str
    desc: str = ""
    render_mode: str
    controller: int
    controller_version: int
    car_id: int
    scenario_ids: List[int]
    view_record: Optional[bool]
    show_game_window: Optional[bool]


class UpdateJob(CreateJob):
    ...


class JobStatusMsg(BaseModel):
    status: str
    detail: Optional[str]
