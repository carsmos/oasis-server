class CarAggregate(object):
    def __init__(self, id,
                 name=None,
                 desc=None,
                 param=None,
                 sensors_snap={},
                 car_snap={}):
        self.name = name
        self.id = id
        self.desc = desc
        self.param = param
        self.sensors_snap = sensors_snap
        self.car_snap = car_snap


