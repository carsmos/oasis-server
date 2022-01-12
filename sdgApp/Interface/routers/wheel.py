from fastapi import APIRouter, status, Depends
from pydantic.typing import List, Optional

from sdgApp.Application.wheel.CommandDTOs import WheelCreateDTO, WheelUpdateDTO
from sdgApp.Application.wheel.RespondsDTOs import WheelGetDTO
from sdgApp.Application.wheel.usercase import WheelCommandUsercase, WheelQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from sdgApp.Infrastructure.MongoDB.FastapiUsers.users_model import UserDB
from sdgApp.Infrastructure.MongoDB.FastapiUsers.manager import current_active_user

router = APIRouter()



@router.post(
    "/wheels",
    status_code=status.HTTP_201_CREATED,
    tags=["Wheels"]
)
async def create_wheel(wheel_create_model: WheelCreateDTO, db = Depends(get_db),
                       user: UserDB = Depends(current_active_user)):
    try:
        wheel_create_dto = wheel_create_model.dict()
        wheel_dto = WheelCommandUsercase(db_session=db, user=user).create_wheel(wheel_create_dto)
        return wheel_dto
    except:
        raise


@router.delete(
    "/wheels/{wheel_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Wheels"]
)
async def delete_wheel(wheel_id:str, db = Depends(get_db),
                       user: UserDB = Depends(current_active_user)):
    try:
        WheelCommandUsercase(db_session=db, user=user).delete_wheel(wheel_id)
    except:
        raise


@router.put(
    "/wheels/{wheel_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Wheels"]
)
async def update_wheel(wheel_id:str, wheel_update_model: WheelUpdateDTO, db = Depends(get_db),
                       user: UserDB = Depends(current_active_user)):
    try:
        wheel_update_dto = wheel_update_model.dict()
        wheel_dto = WheelCommandUsercase(db_session=db, user=user).update_wheel(wheel_id, wheel_update_dto)
        return wheel_dto
    except:
        raise


@router.get(
    "/wheels/{wheel_id}",
    status_code=status.HTTP_200_OK,
    # response_model= WheelGetDTO,
    tags=["Wheels"]
)
async def get_wheel(wheel_id:str, db = Depends(get_db),
                    user: UserDB = Depends(current_active_user)):
    try:
        wheel_dto = WheelQueryUsercase(db_session=db, user=user).get_wheel(wheel_id)
        return wheel_dto
    except:
        raise


@router.get(
    "/wheels",
    status_code=status.HTTP_200_OK,
    # response_model= List[WheelGetDTO],
    tags=["Wheels"]
)
async def list_wheel(car_id: Optional[str] = None,
                     position: Optional[str] = None,
                     db = Depends(get_db),
                     user: UserDB = Depends(current_active_user)):
    try:
        query_param = {}
        if car_id: query_param.update({"car_id": car_id})
        if position: query_param.update({"position": position})

        wheel_dto_lst = WheelQueryUsercase(db_session=db, user=user).list_wheel(query_param=query_param)
        return wheel_dto_lst
    except:
        raise

