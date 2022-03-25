from pydantic import BaseModel
from pydantic.typing import Any
from sdgApp.Domain.environments.envs import EnvsAggregate


class EnvDO(BaseModel):
    id: str
    name: str
    desc: str
    weather_param: dict
    usr_id: Any
    create_time: str = None
    last_modified: str

    def to_entity(self) -> EnvsAggregate:
        return EnvsAggregate(
            id=self.id,
            name=self.name,
            desc=self.desc,
            weather_param=self.weather_param
        )