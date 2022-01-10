from pydantic import BaseModel
from sdgApp.Application.dynamics.CommandDTOs import DynamicsCreateDTO

class DynamicsGetDTO(DynamicsCreateDTO):
    id: str