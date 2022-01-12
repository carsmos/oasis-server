

class ScenariosAggregate(object):
    def __init__(self,
                 id,
                 name=None,
                 desc=None,
                 scenario_param=None
                 ):
        self.id = id
        self.name = name
        self.desc = desc
        self.scenario_param = scenario_param

    def save_DO_shortcut(self, dto_dict: dict):
        self.shortcut_DO = dto_dict
