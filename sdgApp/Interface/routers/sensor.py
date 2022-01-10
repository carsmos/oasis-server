from fastapi import APIRouter, status, Depends
from pydantic.typing import List

from sdgApp.Application.sensor.CommandDTOs import SensorCreateDTO, SensorUpdateDTO
from sdgApp.Application.sensor.RespondsDTOs import SensorGetDTO
from sdgApp.Application.sensor.usercase import SensorCommandUsercase, SensorQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db

router = APIRouter()



@router.post(
    "/sensors",
    status_code=status.HTTP_201_CREATED,
    tags=["Sensors"]
)
async def create_sensor(sensor_create_model: SensorCreateDTO, db = Depends(get_db)):
    try:
        SensorCommandUsercase(db_session=db).create_sensor(sensor_create_model)
    except:
        raise


@router.delete(
    "/sensors/{sensor_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Sensors"]
)
async def delete_sensor(sensor_id:str, db = Depends(get_db)):
    try:
        SensorCommandUsercase(db_session=db).delete_sensor(sensor_id)
    except:
        raise


@router.put(
    "/sensors/{sensor_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Sensors"]
)
async def update_sensor(sensor_id:str, sensor_update_model: SensorUpdateDTO, db = Depends(get_db)):
    try:
        SensorCommandUsercase(db_session=db).update_sensor(sensor_id, sensor_update_model)
    except:
        raise


@router.get(
    "/sensors/{sensor_id}",
    status_code=status.HTTP_200_OK,
    response_model= SensorGetDTO,
    tags=["Sensors"]
)
async def get_sensor(sensor_id:str, db = Depends(get_db)):
    try:
        sensor_dto = SensorQueryUsercase(db_session=db).get_sensor(sensor_id)
        return sensor_dto
    except:
        raise


@router.get(
    "/sensors",
    status_code=status.HTTP_200_OK,
    response_model= List[SensorGetDTO],
    tags=["Sensors"]
)
async def list_sensor(db = Depends(get_db)):
    try:
        sensor_dto_lst = SensorQueryUsercase(db_session=db).list_sensor()
        return sensor_dto_lst
    except:
        raise

