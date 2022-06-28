from pydantic import BaseModel
from pydantic.typing import List
from sdgApp.Application.weather.CommandDTOs import WeatherCreateDTO


class WeatherReadDTO(WeatherCreateDTO):
    id: str
    create_time: str
    last_modified: str


class WeatherResponse(BaseModel):
    total_num: int
    total_page_num: int
    datas: List[WeatherReadDTO]
