from pydantic.typing import Optional, List
from pydantic import BaseModel, Field



class AssembleCreateDTO(BaseModel):
    id: Optional[str]
    name: str = Field(..., example="car_1")
    desc: str
    param: dict
    dynamics_id: Optional[str] = None
    sensors: Optional[List[dict]] = Field(None, example=[{"id": "123", "position":(0.0,0.0,0.0)},
                                                  {"id": "123", "position":(0.0,0.0,0.0)}])
