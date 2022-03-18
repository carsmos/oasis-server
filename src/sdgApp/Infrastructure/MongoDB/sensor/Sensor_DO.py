from pydantic import BaseModel
from pydantic.typing import Any
from sdgApp.Domain.sensor.sensor import SensorAggregate
from datetime import datetime

class SensorDO(BaseModel):
    id: str
    name: str
    type: str
    desc: str
    param: dict
    usr_id: Any
    create_time: str = None
    last_modified: str

    def to_entity(self) -> SensorAggregate:
        return SensorAggregate(id=self.id,
                               name=self.name,
                               type=self.type,
                               desc=self.desc,
                               param=self.param)
