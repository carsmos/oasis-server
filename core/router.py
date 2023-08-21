from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from apps.user.view import router as user_router
from apps.auth.view import router as auth_router
from apps.car.view import router as car_router
from apps.scenario.view import router as scenario_router
from apps.weather.view import router as weather_router
from apps.light.view import router as light_router
from apps.job.view import router as job_router
from apps.upload.view import router as upload_router
from apps.emails.view import router as emails_router
from apps.dynamic.view import router as dynamic_router
from apps.sensor.view import router as sensor_router
from apps.controller.view import router as controller_router
from apps.log.view import router as log_router
from apps.evaluation_criteria.view import router as evaluate_router
from core import settings
from fastapi.responses import JSONResponse

from pydantic import BaseModel
import simplejson
from typing import Any

from utils.response_code import HttpStatus


def handle_special_types(obj: Any) -> Any:
    if isinstance(obj, BaseModel):
        return obj.dict()
    return str(obj)


class MyJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        my_content = {'code': HttpStatus.HTTP_200_OK, 'result': content, 'message': ''}
        v = simplejson.dumps(
            my_content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            default=handle_special_types,
            use_decimal=True,
        ).encode("utf-8")
        return v


api_router = APIRouter(default_response_class=MyJSONResponse)


@api_router.get('/', include_in_schema=False)
async def index():
    return RedirectResponse(url=settings.DOCS_URL)


api_router.include_router(user_router, prefix='/users', tags=["用户"])
api_router.include_router(auth_router, prefix='/auth', tags=["登录注册"])
api_router.include_router(car_router, prefix='/car', tags=['待测车辆'])
api_router.include_router(scenario_router, prefix='/scenario', tags=['场景'])
api_router.include_router(weather_router, prefix='/weather', tags=['天气'])
api_router.include_router(light_router, prefix='/light', tags=['光照'])
api_router.include_router(job_router, prefix='/job', tags=['作业'])
api_router.include_router(upload_router, prefix='/upload', tags=['上传文件'])
api_router.include_router(emails_router, prefix='/emails', tags=['发送邮件'])
api_router.include_router(dynamic_router, prefix='/dynamics', tags=['动力学模型'])
api_router.include_router(sensor_router, prefix='/sensor', tags=['传感器模型'])
api_router.include_router(log_router, prefix='/log', tags=['日志'])
api_router.include_router(evaluate_router, prefix='/evaluate', tags=['评价标准'])
api_router.include_router(controller_router, prefix='/controller', tags=['车辆控制系统'])

__all__ = ["api_router"]
