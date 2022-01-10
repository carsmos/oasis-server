from datetime import datetime
from typing import Optional, Union, List


class ScenariosAggregate(object):
    def __init__(self,
                 dynamic_scene_id=None,
                 script=None,
                 dynamic_scene_name=None,
                 desc=None,
                 create_time=None,
                 ):
        self.dynamic_scene_id = dynamic_scene_id
        self.script = script
        self.dynamic_scene_name = dynamic_scene_name
        self.desc = desc
        self.create_time = create_time

    def save_DO_shortcut(self, dto_dict: dict):
        self.shortcut_DO = dto_dict
