from pydantic import BaseModel
from sdgApp.Application.cars.CommandDTOs import CarCreateDTO

class CarGetDTO(CarCreateDTO):
    id: str

