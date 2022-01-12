from pydantic.typing import Optional, List
from pydantic import BaseModel, Field



class AssembleCreateDTO(BaseModel):
    car_id_with_extraconfig: dict = Field(..., example={"1": {}})
    dynamics_id_with_extraconfig: Optional[dict]
    wheel_id_with_extraconfig: Optional[dict]
    sensor_id_with_extraconfig: Optional[dict]



