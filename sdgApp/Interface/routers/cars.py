from sdgApp.Application.cars.CommandDTOs import CarCreateDTO
from sdgApp.Application.cars.usercase import CarCommandUsercase
from fastapi import APIRouter, status, Depends

router = APIRouter()

@router.post(
    "/cars",
    status_code=status.HTTP_201_CREATED,
    tags=["Cars"]
)
async def create_car(car_create_model: CarCreateDTO):
    try:
        CarCommandUsercase().create_car(car_create_model)
    except:
        raise






