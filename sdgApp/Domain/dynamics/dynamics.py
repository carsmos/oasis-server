class DynamicsAggregate(object):
    def __init__(self, id,
                 name=None,
                 car_name=None,
                 car_id=None,
                 desc=None,
                 param=None):
        self.id = id
        self.name = name
        self.car_name = car_name
        self.car_id = car_id
        self.desc = desc
        self.param = param

    def save_DO_shortcut(self, DO:dict):
        self.shortcut_DO = DO

