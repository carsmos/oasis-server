from pydantic import BaseModel

class DynamicsReadDTO(BaseModel):
    id: str
    name: str
    desc: str
    param: str
    create_time: str
    last_modified: str