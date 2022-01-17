from pydantic.typing import Optional, List
from pydantic import BaseModel, Field



class AssembleCreateDTO(BaseModel):
    car_id: str
    dynamics_id: Optional[str] = None

    wheels: Optional[dict] = Field(None, example={"front_left_wheel":{"id": "123","position":(0.0,0.0,0.0)},
                                                 "front_right_wheel":{"id": "123","position":(0.0,0.0,0.0)},
                                                 "rear_left_wheel":{"id": "123","position":(0.0,0.0,0.0)},
                                                 "rear_right_wheel":{"id": "123","position":(0.0,0.0,0.0)}})
    sensors: Optional[List[dict]] = Field(None, example=[{"id": "123", "position":(0.0,0.0,0.0)},
                                                  {"id": "123", "position":(0.0,0.0,0.0)}])
