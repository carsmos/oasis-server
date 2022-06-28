from typing import Optional
from pydantic import Field, BaseModel


class WeatherCreateDTO(BaseModel):
    name: str = Field(..., example="Cloudy")
    desc: Optional[str] = Field(None, example="It's cloudy weather")
    param: Optional[dict]


class WeatherUpdateDTO(WeatherCreateDTO):
    pass
