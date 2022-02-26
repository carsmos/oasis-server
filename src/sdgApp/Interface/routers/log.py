from fastapi import APIRouter, status, Depends
from typing import Optional
from sdgApp.Application.log.usercase import LogQueryUsercase

from sdgApp.Infrastructure.MongoDB.session_maker import get_db


router = APIRouter()


@router.get(
    "/logs/{task_id}",
    status_code=status.HTTP_200_OK,
    tags=["Logs"]
)
async def get_log(task_id:str, level: Optional[str] = "INFO", db = Depends(get_db)):
    try:
        log_dto = LogQueryUsercase(db_session=db).get_log(task_id, level)
        return log_dto
    except:
        raise