

class EnvsAggregate(object):
    def __init__(self,
                 id,
                 name=None,
                 desc=None,
                 weather_param=None
                 ):
        self.id = id
        self.name = name
        self.desc = desc
        self.weather_param = weather_param

    def save_DO_shortcut(self, dto_dict: dict):
        self.shortcut_DO = dto_dict
