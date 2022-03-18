from pydantic.typing import Optional
from pydantic import BaseModel, Field

from sdgApp.Domain.car.car import CarAggregate
from datetime import datetime

class CarDO(BaseModel):
    id: str
    name: str
    desc: str
    param: dict
    sensors_snap: dict
    car_snap: dict
    usr_id: str = None
    create_time: str = None
    last_modified: str

    def to_entity(self) -> CarAggregate:
        return CarAggregate(
            id=self.id,
            name=self.name,
            desc=self.desc,
            param=self.param,
            sensors_snap=self.sensors_snap,
            car_snap=self.car_snap
        )

