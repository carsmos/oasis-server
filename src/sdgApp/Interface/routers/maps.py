from sdgApp.Application.maps.RespondsDTOs import MapReadDTO
from sdgApp.Infrastructure.MongoDB.session_maker import get_db
from sdgApp.Application.maps.usercase import MapQueryUsercase
from fastapi import APIRouter, status, Depends
from sdgApp.Infrastructure.MongoDB.FastapiUsers.users_model import UserDB
from sdgApp.Infrastructure.MongoDB.FastapiUsers.manager import current_active_user
from typing import List, Union

router = APIRouter()


@router.get(
    "/maps",
    status_code=status.HTTP_200_OK,
    response_model=List[MapReadDTO],
    tags=["Maps"]
)
async def find_all_maps(db=Depends(get_db), user: UserDB = Depends(current_active_user)):
    try:
        return MapQueryUsercase(db_session=db, user=user).find_all_maps()
    except:
        raise


@router.get(
    "/maps/{query_args}",
    status_code=status.HTTP_200_OK,
    response_model=MapReadDTO,
    tags=["Maps"]
)
async def find_specified_map(query_args: Union[int, str], db=Depends(get_db),
                             user: UserDB = Depends(current_active_user)):
    try:
        return MapQueryUsercase(db_session=db, user=user).find_specified_map(query_args)
    except:
        raise
