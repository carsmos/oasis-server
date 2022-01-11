from typing import Optional
from pydantic import Field, BaseModel


class EnvCreateDTO(BaseModel):
    name: str = Field(..., example="env01")
    desc: Optional[str] = Field(None, example="env01")
    param: Optional[dict]


class EnvUpdateDTO(EnvCreateDTO):
    pass
