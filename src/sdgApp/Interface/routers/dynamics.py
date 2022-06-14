from fastapi import APIRouter, status, Depends
from pydantic.typing import List

from sdgApp.Application.dynamics.CommandDTOs import DynamicsCreateDTO, DynamicsUpdateDTO
from sdgApp.Application.dynamics.RespondsDTOs import DynamicsReadDTO, DynamicsResponse
from sdgApp.Application.dynamics.usercase import DynamicsCommandUsercase, DynamicsQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from sdgApp.Interface.FastapiUsers.users_model import UserDB
from sdgApp.Interface.FastapiUsers.manager import current_active_user
from src.sdgApp.Application.log.usercase import except_logger
router = APIRouter()



@router.post(
    "/dynamics",
    status_code=status.HTTP_201_CREATED,
    tags=["Dynamics"]
)
@except_logger("create_dynamics failed .....................")
async def create_dynamics(dynamics_create_model: DynamicsCreateDTO, db = Depends(get_db),
                          user: UserDB = Depends(current_active_user)):
    try:
        await DynamicsCommandUsercase(db_session=db, user=user).create_dynamics(dynamics_create_model)
    except:
        raise


@router.delete(
    "/dynamics/{dynamics_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Dynamics"]
)
@except_logger("delete_dynamics failed .....................")
async def delete_dynamics(dynamics_id:str, db = Depends(get_db),
                          user: UserDB = Depends(current_active_user)):
    try:
        await DynamicsCommandUsercase(db_session=db, user=user).delete_dynamics(dynamics_id)
    except:
        raise


@router.put(
    "/dynamics/{dynamics_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Dynamics"]
)
@except_logger("update_dynamics failed .....................")
async def update_dynamics(dynamics_id:str, dynamics_update_model: DynamicsUpdateDTO, db = Depends(get_db),
                          user: UserDB = Depends(current_active_user)):
    try:
        await DynamicsCommandUsercase(db_session=db, user=user).update_dynamics(dynamics_id, dynamics_update_model)
    except:
        raise


@router.get(
    "/dynamics/{dynamics_id}",
    status_code=status.HTTP_200_OK,
    response_model= DynamicsReadDTO,
    tags=["Dynamics"]
)
@except_logger("get_dynamics failed .....................")
async def get_dynamics(dynamics_id:str, db = Depends(get_db),
                       user: UserDB = Depends(current_active_user)):
    try:
        dynamics_dto = await DynamicsQueryUsercase(db_session=db, user=user).get_dynamics(dynamics_id)
        return dynamics_dto
    except:
        raise


@router.get(
    "/dynamics",
    status_code=status.HTTP_200_OK,
    response_model=DynamicsResponse,
    tags=["Dynamics"]
)
@except_logger("list_dynamics failed .....................")
async def list_dynamics(content: str = "", p_size: int = 15, p_num: int = 1, db=Depends(get_db),
                        user: UserDB = Depends(current_active_user)):
    try:
        dynamics_dto_dic = await DynamicsQueryUsercase(db_session=db, user=user).list_dynamics(p_num, p_size, content)
        return dynamics_dto_dic
    except:
        raise

