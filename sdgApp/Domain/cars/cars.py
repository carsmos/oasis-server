from pydantic import BaseModel, Field
from pydantic.typing import Optional, List




class CarsAggregate(object):
    def __init__(self, id,
                 name=None,
                 desc=None,
                 autosys=None,
                 model=None,
                 physics=None,
                 wheels=None,
                 sensors=None):
        self.name = name
        self.id = id
        self.desc = desc
        self.autosys = autosys
        self.model = model
        self.physics = physics
        self.wheels = wheels
        self.sensors = sensors

    def save_DO_shortcut(self, DO:dict):
        self.shortcut_DO = DO

