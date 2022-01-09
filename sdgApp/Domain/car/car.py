class CarAggregate(object):
    def __init__(self, id,
                 name=None,
                 desc=None,
                 param=None):
        self.name = name
        self.id = id
        self.desc = desc
        self.param = param

    def save_DO_shortcut(self, DO:dict):
        self.shortcut_DO = DO

