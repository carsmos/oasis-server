from fastapi import APIRouter, status, Depends
from pydantic.typing import List

from sdgApp.Application.car.CommandDTOs import CarCreateDTO, CarUpdateDTO
from sdgApp.Application.car.RespondsDTOs import CarReadDTO
from sdgApp.Application.car.usercase import CarCommandUsercase, CarQueryUsercase
from sdgApp.Application.CarFacadeService.CommandDTOs import AssembleCreateDTO
from sdgApp.Application.CarFacadeService.AssembleService import AssembleCarService
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from sdgApp.Infrastructure.MongoDB.FastapiUsers.users_model import UserDB
from sdgApp.Infrastructure.MongoDB.FastapiUsers.manager import current_active_user

router = APIRouter()

##TODO: 整理 try except 包括去重
##TODO: 将输入输出参数dict全部转化为model 小dto dict 转换为大 DTO model


@router.post(
    "/cars",
    status_code=status.HTTP_201_CREATED,
    tags=["Cars"]
)
async def create_car(car_create_model: CarCreateDTO, db = Depends(get_db),
                     user: UserDB = Depends(current_active_user)):
    try:
        CarCommandUsercase(db_session=db, user=user).create_car(car_create_model)
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
        CarCommandUsercase(db_session=db, user=user).delete_car(car_id)
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
        CarCommandUsercase(db_session=db, user=user).update_car(car_id, car_update_model)
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
        car_dto = CarQueryUsercase(db_session=db, user=user).get_car(car_id)
        return car_dto
    except:
        raise


@router.get(
    "/cars",
    status_code=status.HTTP_200_OK,
    response_model= List[CarReadDTO],
    tags=["Cars"]
)
async def list_car(skip: int = 0,  db=Depends(get_db),
                   user: UserDB = Depends(current_active_user)):
    try:
        car_dto_lst = CarQueryUsercase(db_session=db, user=user).list_car(skip)
        return car_dto_lst
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
        AssembleCarService(assemble_create_model, db_session=db, user=user)
    except:
        raise

@router.get(
    "/carla/cars/{car_id}",
    status_code=status.HTTP_200_OK,
    response_model= CarReadDTO,
    tags=["Carla"]
)
async def get_car(car_id:str, db = Depends(get_db)):
    try:
        car_dto = CarQueryUsercase(db_session=db, user=None).get_car(car_id)
        return car_dto
    except:
        raise