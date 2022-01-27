from pydantic import BaseModel
from sdgApp.Application.wheel.CommandDTOs import WheelCreateDTO

class WheelGetDTO(WheelCreateDTO):
    id: str