from pydantic.typing import Optional, List
from pydantic import BaseModel, Field


class MapModel(BaseModel):
    map_id: int = Field(..., example=1)
    map_name: str = Field(..., example="Town01")


class MapCreateDTO(BaseModel):
    pass


class MapUpdateDTO(BaseModel):
    pass


class MapDeleteDTO(BaseModel):
    pass
