

class DynamicScenesAggregate(object):
    def __init__(self,
                 id,
                 name=None,
                 desc=None,
                 scene_script=None,
                 ):
        self.id = id
        self.name = name
        self.desc = desc
        self.scene_script = scene_script

    def save_DO_shortcut(self, dto_dict: dict):
        self.shortcut_DO = dto_dict
