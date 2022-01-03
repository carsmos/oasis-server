from pydantic import BaseModel, Field
from pydantic.typing import Optional, List




class CarsAggregate(object):
    def __init__(self,
                 id:str,
                 name:str,
                 autosys:str,
                 model_dict:dict,
                 physics_dict:dict,
                 wheels_dict:dict,
                 sensors_list:List,
                 desc=None
                 ):
        self.id = id
        self.name = name
        self.autosys = autosys
        self.model_dict = model_dict
        self.physics_dict = physics_dict
        self.wheels_dict = wheels_dict
        self.sensors_list = sensors_list
        self.desc = desc

    def save_DO_shortcut(self, dto_dict:dict):
        self.shortcut_DO = dto_dict
