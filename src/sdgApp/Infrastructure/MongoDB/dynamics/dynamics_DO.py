from pydantic import BaseModel, Field
from pydantic.typing import Any
from sdgApp.Domain.dynamics.dynamics import DynamicsAggregate
from datetime import datetime

class DynamicsDO(BaseModel):
    id: str
    name: str
    desc: str
    param: dict
    usr_id: Any
    create_time: str = None
    last_modified: str

    def to_entity(self) -> DynamicsAggregate:
        return DynamicsAggregate(
            id=self.id,
            name=self.name,
            desc=self.desc,
            param=self.param
        )
