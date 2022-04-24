from pydantic import BaseModel
from pydantic.typing import List, Optional


class JobReadDTO(BaseModel):
    id: str
    name: str
    desc: str
    create_time: str
    last_modified: str
    task_list: List[dict]


class JobStatusMsg(BaseModel):
    status: str
    detail: Optional[str]


class JobsResponse(BaseModel):
    total_num: int
    total_page_num: int
    datas: List[JobReadDTO]