from fastapi import APIRouter, status, Depends
from typing import Optional
from sdgApp.Application.log.usercase import LogQueryUsercase

from sdgApp.Infrastructure.MongoDB.session_maker import get_db

from sdgApp.Application.log.usercase import except_logger
router = APIRouter()


@router.get(
    "/logs/{task_id}",
    status_code=status.HTTP_200_OK,
    tags=["Logs"]
)
@except_logger("list_log failed .....................")
async def list_log(task_id:str, level: Optional[str] = "INFO", db = Depends(get_db)):
    try:
        log_dto_lst = await LogQueryUsercase(db_session=db).list_log(task_id, level)
        return log_dto_lst
    except:
        raise