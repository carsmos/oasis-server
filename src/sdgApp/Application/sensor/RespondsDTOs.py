from pydantic import BaseModel

class SensorReadDTO(BaseModel):
    id: str
    name: str
    type: str
    desc: str
    param: dict
    create_time: str
    last_modified: str
