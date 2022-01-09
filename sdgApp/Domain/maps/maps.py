

class MapsAggregate(object):
    def __init__(self, map_id=None, map_name=None):
        self.map_id = map_id
        self.map_name = map_name

    def save_DO_shortcut(self, DO:dict):
        self.shortcut_DO = DO
