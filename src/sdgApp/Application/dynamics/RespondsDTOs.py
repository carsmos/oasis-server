from pydantic import BaseModel

class DynamicsReadDTO(BaseModel):
    id: str
    name: str
    desc: str
    param: dict
    create_time: str
    last_modified: str