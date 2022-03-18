from pydantic import BaseModel

class CarReadDTO(BaseModel):
    id: str
    name: str
    desc: str
    param: dict
    sensors_snap: dict
    car_snap: dict
    create_time: str = None
    last_modified: str


