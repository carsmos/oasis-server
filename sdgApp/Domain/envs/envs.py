

class EnvsAggregate(object):
    def __init__(self,
                 env_id=None,
                 env_name=None,
                 desc=None,
                 create_time=None,
                 param=None
                 ):
        self.env_id = env_id
        self.env_name = env_name
        self.create_time = create_time
        self.desc = desc
        self.parma = param

    def save_DO_shortcut(self, dto_dict: dict):
        self.shortcut_DO = dto_dict
