from datetime import datetime
from typing import Optional, Union, List


class ScenariosAggregate(object):
    def __init__(self,
                 dynamic_scene_id: Optional[str],
                 script: str,
                 scenario_name: str,
                 desc: Optional[str],
                 tags: Optional[List[str]],
                 create_time: Union[datetime, str],
                 language: Optional[str],
                 ):
        self.dynamic_scene_id = dynamic_scene_id
        self.script = script
        self.scenario_name = scenario_name
        self.desc = desc
        self.tags = tags
        self.create_time = create_time
        self.language = language

    def save_DO_shortcut(self, dto_dict: dict):
        self.shortcut_DO = dto_dict
