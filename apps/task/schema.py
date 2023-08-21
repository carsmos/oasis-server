from pydantic import BaseModel
from pydantic.typing import List


class CarSensor(BaseModel):
    car_id: str
    sensor_id: str
    name: str
    type: str
    position_x: int
    positon_y: int
    position_z: int
    roll: int
    pitch: int
    yaw: int


class Create(BaseModel):
    name: str = ''
    desc: str = ''
    color: str = ''
    light_state: str = ''
    type: str = ''
    dynamic_id: str = ''
    render_mode: str = ''
    car_sensors: List[CarSensor] = []


