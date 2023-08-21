from typing import List

from fastapi import APIRouter, Depends, status, HTTPException, Request, Body, Query
from tortoise.expressions import Q
from core.settings import TIMES
from apps.auth.auth_casbin import AuthorityRole
from apps.weather.model import Weathers_Pydantic, Weathers
from core.middleware import limiter
from utils.auth import request
from utils.utils import paginate

router = APIRouter()


@router.post(
    "/weather",
    summary='创建天气',
    tags=["weather"]
)
@limiter.limit("%d/minute" %TIMES)
async def create_weather(request: Request, weather_create_mode: Weathers_Pydantic):
    user = request.state.user
    assert not await Weathers.filter(Q(company_id=user.company_id) | Q(system_data=1), name=weather_create_mode.name,
                                     invalid=0).first(), '天气名称已存在，请更换'
    weather = Weathers(**weather_create_mode.dict())
    weather.user_id = user.id
    weather.company_id = user.company_id
    await weather.save()
    return weather


@router.delete("/weather",
               summary='删除天气',
               tags=["weather"],
               dependencies=[Depends(AuthorityRole('admin'))])
@limiter.limit("%d/minute" %TIMES)
async def delete_weather(request: Request, weather_ids: List[int] = Body(..., embed=True)):
    user = request.state.user
    weathers = await Weathers.filter(Q(company_id=user.company_id) | Q(system_data=1), id__in=weather_ids,
                                     invalid=0).all()
    assert len(weathers) == len(weather_ids), '存在错误的天气id'
    for weather in weathers:
        assert not weather.system_data, '系统内置天气不可删除'
        weather.invalid = weather.id
    await Weathers.bulk_update(weathers, fields=["invalid"])
    return


@router.put(
    "/weather/{weather_id}",
    summary='更新天气',
    tags=["weather"]
)
@limiter.limit("%d/minute" %TIMES)
async def update_weather(request: Request, weather_id: int, weather_create_mode: Weathers_Pydantic):
    user = request.state.user
    weather_info = await Weathers.filter(Q(company_id=user.company_id) | Q(system_data=1),id=weather_id,
                                         invalid=0).first()
    assert weather_info, '天气信息不存在'
    assert not weather_info.system_data, '系统内置天气参数不可修改'
    if weather_create_mode.name != weather_info.name:
        assert not await Weathers.filter(Q(company_id=user.company_id) | Q(system_data=1),name=weather_create_mode.name,
                                         invalid=0).first(), "天气名称已存在，请更换"
    await weather_info.update_from_dict(weather_create_mode.dict()).save()
    return weather_info


@router.get(
    "/weather/{weather_id}",
    summary='查找指定id天气',
    tags=["weather"]
)
async def find_specified_weather(weather_id: str):
    user = request.state.user
    weather_info = await Weathers.filter(Q(company_id=user.company_id) | Q(system_data=1), id=weather_id,
                                         invalid=0).first()
    assert weather_info, '天气信息不存在'
    return weather_info


@router.get(
    "/weather",
    summary='查找所有天气',
    tags=["weather"]
)
async def find_all_weather(content: str = '', pagesize: int = 15, pagenum: int = 1):
    user = request.state.user
    weather_model = Weathers.filter(Q(company_id=user.company_id) | Q(system_data=1), invalid=0)
    if content:
        weather_model = weather_model.filter(Q(name__contains=content) | Q(desc__contains=content))

    total_num = await weather_model.count()
    if pagesize == 0:
        data = await weather_model.all()
    else:
        data = await weather_model.limit(pagesize).offset(max(0, pagenum - 1) * pagesize).all()
    pageinfo = paginate(total_num, pagesize)
    data = sorted(data, key=lambda v: v.modified_at, reverse=True)
    return {"pageinfo": pageinfo, "datas": data}
