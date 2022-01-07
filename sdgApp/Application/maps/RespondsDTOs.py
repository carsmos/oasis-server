from pydantic import BaseModel, Field


class MapReadDTO(BaseModel):
    map_id: int = Field(..., example=1)
    map_name: str = Field(..., example="Town01")
