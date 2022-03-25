from pydantic import BaseModel
from pydantic.typing import Any
from sdgApp.Domain.dynamic_scenes.dynamic_scenes import DynamicScenesAggregate


class DynamicSceneDO(BaseModel):
    id: str
    name: str
    desc: str
    scene_script: str
    usr_id: Any
    create_time: str = None
    last_modified: str
    type: str

    def to_entity(self) -> DynamicScenesAggregate:
        return DynamicScenesAggregate(
            id=self.id,
            name=self.name,
            desc=self.desc,
            scene_script=self.scene_script,
            type=self.type
        )
