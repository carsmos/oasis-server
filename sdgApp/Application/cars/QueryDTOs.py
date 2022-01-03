from pydantic import BaseModel, Field
from pydantic.typing import Optional

class CarFindDTO(BaseModel):
    id: str