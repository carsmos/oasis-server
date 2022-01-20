from pydantic import BaseModel, Field
from pydantic.typing import List

class TaskCreateDTO(BaseModel):
    name: str
    desc: str
    car_id: str
    car_name: str
    scenario_id: str
    scenario_name: str

class TaskUpdateDTO(TaskCreateDTO):
    id: str


class JobCreateDTO(BaseModel):
    name: str = Field(..., example="job_1")
    desc: str
    task_list: List[TaskCreateDTO]


class JobUpdateDTO(BaseModel):
    name: str = Field(..., example="job_1")
    desc: str
    task_list: List[TaskUpdateDTO]