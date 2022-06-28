from pydantic import BaseModel
from pydantic.typing import Any
from sdgApp.Domain.light.lights import LightAggregate


class lightDO(BaseModel):
    id: str
    name: str
    desc: str
    param: dict
    usr_id: Any
    create_time: str = None
    last_modified: str

    def to_entity(self) -> LightAggregate:
        return LightAggregate(
            id=self.id,
            name=self.name,
            desc=self.desc,
            param=self.param
        )