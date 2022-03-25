

class DynamicScenesAggregate(object):
    def __init__(self,
                 id,
                 name=None,
                 desc=None,
                 scene_script=None,
                 type=None
                 ):
        self.id = id
        self.name = name
        self.desc = desc
        self.scene_script = scene_script
        self.type = type
