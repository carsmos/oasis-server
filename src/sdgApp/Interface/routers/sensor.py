from fastapi import APIRouter, status, Depends
from pydantic.typing import List, Optional

from sdgApp.Application.sensor.CommandDTOs import SensorCreateDTO, SensorUpdateDTO
from sdgApp.Application.sensor.RespondsDTOs import SensorReadDTO
from sdgApp.Application.sensor.usercase import SensorCommandUsercase, SensorQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from sdgApp.Interface.FastapiUsers.users_model import UserDB
from sdgApp.Interface.FastapiUsers.manager import current_active_user

router = APIRouter()



@router.post(
    "/sensors",
    status_code=status.HTTP_201_CREATED,
    tags=["Sensors"]
)
async def create_sensor(sensor_create_model: SensorCreateDTO, db = Depends(get_db),
                        user: UserDB = Depends(current_active_user)):
    try:
        SensorCommandUsercase(db_session=db, user=user).create_sensor(sensor_create_model)
    except:
        raise


@router.delete(
    "/sensors/{sensor_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Sensors"]
)
async def delete_sensor(sensor_id:str, db = Depends(get_db),
                        user: UserDB = Depends(current_active_user)):
    try:
        SensorCommandUsercase(db_session=db, user=user).delete_sensor(sensor_id)
    except:
        raise


@router.put(
    "/sensors/{sensor_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Sensors"]
)
async def update_sensor(sensor_id:str, sensor_update_model: SensorUpdateDTO, db = Depends(get_db),
                        user: UserDB = Depends(current_active_user)):
    try:
        SensorCommandUsercase(db_session=db, user=user).update_sensor(sensor_id, sensor_update_model)
    except:
        raise


@router.get(
    "/sensors/{sensor_id}",
    status_code=status.HTTP_200_OK,
    response_model= SensorReadDTO,
    tags=["Sensors"]
)
async def get_sensor(sensor_id:str, db = Depends(get_db),
                     user: UserDB = Depends(current_active_user)):
    try:
        sensor_dto = SensorQueryUsercase(db_session=db, user=user).get_sensor(sensor_id)
        return sensor_dto
    except:
        raise


@router.get(
    "/sensors",
    status_code=status.HTTP_200_OK,
    response_model= List[SensorReadDTO],
    tags=["Sensors"]
)
async def list_sensor(skip: int = 0, sensor_type: Optional[str] = None,
                      db= Depends(get_db),
                      user: UserDB = Depends(current_active_user)):
    try:
        query_param = {}
        if sensor_type: query_param.update({"type": sensor_type})

        sensor_dto_lst = SensorQueryUsercase(db_session=db, user=user).list_sensor(skip, query_param=query_param)
        return sensor_dto_lst
    except:
        raise

