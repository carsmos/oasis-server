from fastapi import APIRouter, status, Depends
from pydantic.typing import List, Optional

from sdgApp.Application.dynamics.CommandDTOs import DynamicsCreateDTO, DynamicsUpdateDTO
from sdgApp.Application.dynamics.RespondsDTOs import DynamicsGetDTO
from sdgApp.Application.dynamics.usercase import DynamicsCommandUsercase, DynamicsQueryUsercase
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from sdgApp.Infrastructure.MongoDB.FastapiUsers.users_model import UserDB
from sdgApp.Infrastructure.MongoDB.FastapiUsers.manager import current_active_user

router = APIRouter()



@router.post(
    "/dynamics",
    status_code=status.HTTP_201_CREATED,
    tags=["Dynamics"]
)
async def create_dynamics(dynamics_create_model: DynamicsCreateDTO, db = Depends(get_db),
                          user: UserDB = Depends(current_active_user)):
    try:
        dynamics_create_dto = dynamics_create_model.dict()
        DynamicsCommandUsercase(db_session=db, user=user).create_dynamics(dynamics_create_dto)
    except:
        raise


@router.delete(
    "/dynamics/{dynamics_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Dynamics"]
)
async def delete_dynamics(dynamics_id:str, db = Depends(get_db),
                          user: UserDB = Depends(current_active_user)):
    try:
        DynamicsCommandUsercase(db_session=db, user=user).delete_dynamics(dynamics_id)
    except:
        raise


@router.put(
    "/dynamics/{dynamics_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Dynamics"]
)
async def update_dynamics(dynamics_id:str, dynamics_update_model: DynamicsUpdateDTO, db = Depends(get_db),
                          user: UserDB = Depends(current_active_user)):
    try:
        dynamics_update_dto = dynamics_update_model.dict()
        DynamicsCommandUsercase(db_session=db, user=user).update_dynamics(dynamics_id, dynamics_update_dto)
    except:
        raise


@router.get(
    "/dynamics/{dynamics_id}",
    status_code=status.HTTP_200_OK,
    # response_model= DynamicsGetDTO,
    tags=["Dynamics"]
)
async def get_dynamics(dynamics_id:str, db = Depends(get_db),
                       user: UserDB = Depends(current_active_user)):
    try:
        dynamics_dto = DynamicsQueryUsercase(db_session=db, user=user).get_dynamics(dynamics_id)
        return dynamics_dto
    except:
        raise


@router.get(
    "/dynamics",
    status_code=status.HTTP_200_OK,
    # response_model= List[DynamicsGetDTO],
    tags=["Dynamics"]
)
async def list_dynamics(car_id: Optional[str] = None,
                        db = Depends(get_db),
                        user: UserDB = Depends(current_active_user)):
    try:
        query_param = {}
        if car_id: query_param.update({"car_id": car_id})

        dynamics_dto_lst = DynamicsQueryUsercase(db_session=db, user=user).list_dynamics(query_param=query_param)
        return dynamics_dto_lst
    except:
        raise

