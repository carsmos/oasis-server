class CarAggregate(object):
    def __init__(self, id,
                 name=None,
                 desc=None,
                 param=None,
                 sensors_snap=None,
                 car_snap=None):
        self.name = name
        self.id = id
        self.desc = desc
        self.param = param
        self.sensors_snap = sensors_snap
        self.car_snap = car_snap

    def save_DO_shortcut(self, DO:dict):
        self.shortcut_DO = DO

