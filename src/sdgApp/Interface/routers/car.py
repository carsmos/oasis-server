from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from pydantic.typing import List

from sdgApp.Application.car.CommandDTOs import CarCreateDTO, CarUpdateDTO
from sdgApp.Application.car.RespondsDTOs import CarReadDTO, CarsResponse
from sdgApp.Application.car.usercase import CarCommandUsercase, CarQueryUsercase
from sdgApp.Application.CarFacadeService.CommandDTOs import AssembleCreateDTO
from sdgApp.Application.CarFacadeService.AssembleService import AssembleCarService
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from sdgApp.Interface.FastapiUsers.users_model import UserDB
from sdgApp.Interface.FastapiUsers.manager import current_active_user

from sdgApp.Domain.dynamics.dynamics_exceptions import DynamicsNotFoundError
from sdgApp.Domain.sensor.sensor_exceptions import SensorNotFoundError

router = APIRouter()

##TODO: 整理 try except 包括去重



@router.post(
    "/cars",
    status_code=status.HTTP_201_CREATED,
    tags=["Cars"]
)
async def create_car(car_create_model: CarCreateDTO, db = Depends(get_db),
                     user: UserDB = Depends(current_active_user)):
    try:
        await CarCommandUsercase(db_session=db, user=user).create_car(car_create_model)
    except:
        raise


@router.delete(
    "/cars/{car_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Cars"]
)
async def delete_car(car_id:str, db = Depends(get_db),
                     user: UserDB = Depends(current_active_user)):
    try:
        await CarCommandUsercase(db_session=db, user=user).delete_car(car_id)
    except:
        raise


@router.put(
    "/cars/{car_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Cars"]
)
async def update_car(car_id:str, car_update_model: CarUpdateDTO, db = Depends(get_db),
                     user: UserDB = Depends(current_active_user)):
    try:
        await CarCommandUsercase(db_session=db, user=user).update_car(car_id, car_update_model)
    except:
        raise


@router.get(
    "/cars/{car_id}",
    status_code=status.HTTP_200_OK,
    response_model= CarReadDTO,
    tags=["Cars"]
)
async def get_car(car_id:str, db = Depends(get_db),
                  user: UserDB = Depends(current_active_user)):
    try:
        car_dto = await CarQueryUsercase(db_session=db, user=user).get_car(car_id)
        return car_dto
    except:
        raise


@router.get(
    "/cars",
    status_code=status.HTTP_200_OK,
    response_model=CarsResponse,
    tags=["Cars"]
)
async def list_car(skip: int = 1, db=Depends(get_db),
                   user: UserDB = Depends(current_active_user)):
    try:
        car_dto_dic = await CarQueryUsercase(db_session=db, user=user).list_car(skip)
        return car_dto_dic
    except:
        raise

@router.put(
    "/cars-assemble",
    status_code=status.HTTP_201_CREATED,
    tags=["Cars"]
)
async def assemble_car(assemble_create_model: AssembleCreateDTO, db = Depends(get_db),
                     user: UserDB = Depends(current_active_user)):
    try:
        await AssembleCarService(assemble_create_model, db_session=db, user=user)
    except DynamicsNotFoundError as e:
        return JSONResponse(status_code=200, content={"status": "fail", "detail": e.message})
    except SensorNotFoundError as e:
        return JSONResponse(status_code=200, content={"status": "fail", "detail": e.message})
    except:
        raise

@router.post(
    "/overview",
    status_code=status.HTTP_200_OK,
    response_model=CarReadDTO,
    tags=["Cars"]
)
async def overview(assemble_create_model: AssembleCreateDTO, db = Depends(get_db),
                     user: UserDB = Depends(current_active_user)):
    try:
        overview_dto = await AssembleCarService(assemble_create_model, db_session=db, user=user, overview_only=True)
        return overview_dto
    except:
        raise