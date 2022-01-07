from pydantic import BaseModel, Field
from typing import Union, Optional


class MapFindDTO(BaseModel):
    map_id: Optional[int] = Field(..., example=1)
    map_name: Optional[str] = Field(..., example="Town01")
