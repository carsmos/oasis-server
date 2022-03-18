from pydantic import BaseModel, Field


class DynamicsCreateDTO(BaseModel):
    name: str = Field(..., example="Dynamics_1")
    desc: str
    param: dict


class DynamicsUpdateDTO(DynamicsCreateDTO):
    ...
