from pydantic import BaseModel, Field
from pydantic.typing import Optional

class SensorListDTO(BaseModel):
    id: Optional[str]