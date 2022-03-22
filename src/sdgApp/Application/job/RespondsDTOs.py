from pydantic import BaseModel
from pydantic.typing import List

class JobReadDTO(BaseModel):
    id: str
    name: str
    desc: str
    create_time: str
    last_modified: str
    task_list: List[dict]

class JobStatusMsg(BaseModel):
    status: str