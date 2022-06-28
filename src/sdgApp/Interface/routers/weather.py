from sdgApp.Application.weather.RespondsDTOs import WeatherReadDTO, WeatherResponse
from sdgApp.Application.weather.CommandDTOs import WeatherCreateDTO, WeatherUpdateDTO
from sdgApp.Application.weather.usercase import WeatherCommandUsercase, WeatherQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from fastapi import APIRouter, status, Depends
from sdgApp.Interface.FastapiUsers.users_model import UserDB
from sdgApp.Interface.FastapiUsers.manager import current_active_user
from typing import List
from sdgApp.Application.log.usercase import except_logger

router = APIRouter()


@router.post(
    "/weather",
    status_code=status.HTTP_201_CREATED,
    response_model=WeatherReadDTO,
    tags=["weather"]
)
@except_logger("creat_weather failed .....................")
async def creat_weather(weather_create_model: WeatherCreateDTO, db=Depends(get_db),
                        user: UserDB = Depends(current_active_user)):
    try:
        await WeatherCommandUsercase(db_session=db, user=user).create_weather(weather_create_model)
    except:
        raise


@router.delete("/weather/{weather_ids}",
               status_code=status.HTTP_202_ACCEPTED,
               tags=["weather"])
@except_logger("delete_weather failed .....................")
async def delete_weather(weather_ids: str, db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        await WeatherCommandUsercase(db_session=db, user=user).delete_weather(weather_ids)
    except:
        raise


@router.put(
    "/weather/{weather_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=WeatherReadDTO,
    tags=["weather"]
)
@except_logger("update_weather failed .....................")
async def update_weather(weather_id: str, env_update_model: WeatherUpdateDTO, db=Depends(get_db),
                         user: UserDB = Depends(current_active_user)):
    try:
        await WeatherCommandUsercase(db_session=db, user=user).update_weather(weather_id, env_update_model)
    except:
        raise


@router.get(
    "/weather/{weather_id}",
    status_code=status.HTTP_200_OK,
    response_model=WeatherReadDTO,
    tags=["weather"]
)
@except_logger("find_specified_weather failed .....................")
async def find_specified_weather(weather_id: str, db=Depends(get_db),
                                 user: UserDB = Depends(current_active_user)):
    try:
        return await WeatherQueryUsercase(db_session=db, user=user).find_specified_weather(weather_id)
    except:
        raise


@router.get(
    "/weather",
    status_code=status.HTTP_200_OK,
    response_model=WeatherResponse,
    tags=["weather"]
)
@except_logger("find_all_weather failed .....................")
async def find_all_weather(content: str = '', p_size: int = 15, p_num: int = 1, db=Depends(get_db),
                           user: UserDB = Depends(current_active_user)):
    try:
        return await WeatherQueryUsercase(db_session=db, user=user).find_all_weather(p_num, p_size, content)
    except:
        raise
