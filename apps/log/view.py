import utils.utils

from fastapi import APIRouter, status
from utils.auth import request
from typing import Optional
from apps.log.model import Logs

router = APIRouter()


@router.get("/get_logs",
            summary='获取日志表',
            tags=["Logs"])
async def list_log(task_id: str, level: Optional[str] = "INFO"):
    logs = await Logs.filter(task_id=task_id, log_level=level).all()
    return logs