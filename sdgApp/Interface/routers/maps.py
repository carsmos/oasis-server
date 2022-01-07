from sdgApp.Application.maps.RespondsDTOs import MapReadDTO
from sdgApp.Application.maps.QueryDTOs import MapFindDTO
from sdgApp.Application.maps.usercase import MapQueryUsercase
from fastapi import APIRouter, status
from typing import List, Union

router = APIRouter()


@router.get(
    "/maps",
    status_code=status.HTTP_200_OK,
    response_model=List[MapReadDTO],
    tags=["Maps"]
)
async def find_all_maps():
    try:
        return MapQueryUsercase().find_all_maps()
    except:
        raise


@router.get(
    "/maps/{query_args}",
    status_code=status.HTTP_200_OK,
    response_model=MapReadDTO,
    tags=["Maps"]
)
async def find_specified_map(query_args: Union[int, str]):
    try:
        return MapQueryUsercase().find_specified_map(query_args)
    except:
        raise
