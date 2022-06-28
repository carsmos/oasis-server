from typing import Optional
from pydantic import Field, BaseModel


class LightCreateDTO(BaseModel):
    name: str = Field(..., example="Noon")
    desc: Optional[str] = Field(None, example="At noon")
    param: Optional[dict]


class LightUpdateDTO(LightCreateDTO):
    pass
