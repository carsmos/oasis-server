from pydantic import BaseModel
from sdgApp.Application.sensor.CommandDTOs import SensorCreateDTO

class SensorGetDTO(SensorCreateDTO):
    id: str