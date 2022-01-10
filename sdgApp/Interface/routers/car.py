from fastapi import APIRouter, status, Depends
from pydantic.typing import List

from sdgApp.Application.car.CommandDTOs import CarCreateDTO, CarUpdateDTO
from sdgApp.Application.car.RespondsDTOs import CarGetDTO
from sdgApp.Application.car.usercase import CarCommandUsercase, CarQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db

router = APIRouter()

##TODO: facade  外部Interface接口 内部service接口
##TODO: 参考 fastapi-user 添加权限系统
##TODO: 整理 try except
##TODO：插入时间


@router.post(
    "/cars",
    status_code=status.HTTP_201_CREATED,
    tags=["Cars"]
)
async def create_car(car_create_model: CarCreateDTO, db = Depends(get_db)):
    try:
        CarCommandUsercase(db_session=db).create_car(car_create_model)
    except:
        raise


@router.delete(
    "/cars/{car_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Cars"]
)
async def delete_car(car_id:str, db = Depends(get_db)):
    try:
        CarCommandUsercase(db_session=db).delete_car(car_id)
    except:
        raise


@router.put(
    "/cars/{car_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Cars"]
)
async def update_car(car_id:str, car_update_model: CarUpdateDTO, db = Depends(get_db)):
    try:
        CarCommandUsercase(db_session=db).update_car(car_id, car_update_model)
    except:
        raise


@router.get(
    "/cars/{car_id}",
    status_code=status.HTTP_200_OK,
    response_model= CarGetDTO,
    tags=["Cars"]
)
async def get_car(car_id:str, db = Depends(get_db)):
    try:
        car_dto = CarQueryUsercase(db_session=db).get_car(car_id)
        return car_dto
    except:
        raise


@router.get(
    "/cars",
    status_code=status.HTTP_200_OK,
    response_model= List[CarGetDTO],
    tags=["Cars"]
)
async def list_car(db = Depends(get_db)):
    try:
        car_dto_lst = CarQueryUsercase(db_session=db).list_car()
        return car_dto_lst
    except:
        raise




