from sdgApp.Application.light.RespondsDTOs import LightReadDTO, LightResponse
from sdgApp.Application.light.CommandDTOs import LightCreateDTO, LightUpdateDTO
from sdgApp.Application.light.usercase import LightCommandUsercase, LightQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from fastapi import APIRouter, status, Depends
from sdgApp.Interface.FastapiUsers.users_model import UserDB
from sdgApp.Interface.FastapiUsers.manager import current_active_user
from typing import List
from sdgApp.Application.log.usercase import except_logger

router = APIRouter()


@router.post(
    "/light",
    status_code=status.HTTP_201_CREATED,
    response_model=LightReadDTO,
    tags=["light"]
)
@except_logger("creat_light failed .....................")
async def create_light(light_create_model: LightCreateDTO, db=Depends(get_db),
                        user: UserDB = Depends(current_active_user)):
    try:
        light_id = await LightCommandUsercase(db_session=db, user=user).create_light(light_create_model)
        return await find_specified_light(light_id, db, user)
    except:
        raise


@router.delete("/light/{light_ids}",
               status_code=status.HTTP_202_ACCEPTED,
               tags=["light"])
@except_logger("delete_light failed .....................")
async def delete_light(light_ids: str, db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        await LightCommandUsercase(db_session=db, user=user).delete_light(light_ids)
    except:
        raise


@router.put(
    "/light/{light_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=LightReadDTO,
    tags=["light"]
)
@except_logger("update_light failed .....................")
async def update_light(light_id: str, light_update_model: LightUpdateDTO, db=Depends(get_db),
                         user: UserDB = Depends(current_active_user)):
    try:
        await LightCommandUsercase(db_session=db, user=user).update_light(light_id, light_update_model)
        return await find_specified_light(light_id, db, user)
    except:
        raise


@router.get(
    "/light/{light_id}",
    status_code=status.HTTP_200_OK,
    response_model=LightReadDTO,
    tags=["light"]
)
@except_logger("find_specified_light failed .....................")
async def find_specified_light(light_id: str, db=Depends(get_db),
                                 user: UserDB = Depends(current_active_user)):
    try:
        return await LightQueryUsercase(db_session=db, user=user).find_specified_light(light_id)
    except:
        raise


@router.get(
    "/light",
    status_code=status.HTTP_200_OK,
    response_model=LightResponse,
    tags=["light"]
)
@except_logger("find_all_light failed .....................")
async def find_all_light(content: str = '', p_size: int = 15, p_num: int = 1, db=Depends(get_db),
                           user: UserDB = Depends(current_active_user)):
    try:
        return await LightQueryUsercase(db_session=db, user=user).find_all_light(p_num, p_size, content)
    except:
        raise
