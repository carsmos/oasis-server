from pydantic import BaseModel, Field
from pydantic.typing import List


class CarSensor(BaseModel):
    sensor_id: int
    nick_name: str = ''
    type: str
    position_x: float
    position_y: float
    position_z: float
    roll: float
    pitch: float
    yaw: float
    data_record: bool
    semantic: bool
    instance: bool


class CarModel(BaseModel):
    name: str = Field(..., example="car_1")
    desc: str = ''
    vehicle_color: str = ''
    light_state: str = ''
    type: str = ''
    dynamics_id: int
    render_mode: str = 'render'
    sensors: List[CarSensor] = []


