from pydantic import BaseModel
from sdgApp.Application.car.CommandDTOs import CarCreateDTO

class CarGetDTO(CarCreateDTO):
    id: str

