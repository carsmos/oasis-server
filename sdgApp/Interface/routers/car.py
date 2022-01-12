from fastapi import APIRouter, status, Depends
from pydantic.typing import List

from sdgApp.Application.car.CommandDTOs import CarCreateDTO, CarUpdateDTO
from sdgApp.Application.car.RespondsDTOs import CarGetDTO
from sdgApp.Application.car.usercase import CarCommandUsercase, CarQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from sdgApp.Infrastructure.MongoDB.FastapiUsers.users_model import UserDB
from sdgApp.Infrastructure.MongoDB.FastapiUsers.manager import current_active_user

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
async def create_car(car_create_model: CarCreateDTO, db = Depends(get_db),
                     user: UserDB = Depends(current_active_user)):
    try:
        car_create_dto = car_create_model.dict()
        CarCommandUsercase(db_session=db, user=user).create_car(car_create_dto)
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
        car_update_dto = car_update_model.dict()
        CarCommandUsercase(db_session=db, user=user).update_car(car_id, car_update_dto)
    except:
        raise


@router.get(
    "/cars/{car_id}",
    status_code=status.HTTP_200_OK,
    # response_model= CarGetDTO,
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
    # response_model= List[CarGetDTO],
    tags=["Cars"]
)
async def list_car(db = Depends(get_db),
                   user: UserDB = Depends(current_active_user)):
    try:
        car_dto_lst = CarQueryUsercase(db_session=db, user=user).list_car()
        return car_dto_lst
    except:
        raise


