from typing import List

from fastapi import APIRouter, Depends, status, HTTPException, Request, Body, Query, Form
from tortoise.expressions import Q

from apps.auth.auth_casbin import AuthorityRole
from apps.light.model import Lights_Pydantic, Lights
from core.middleware import limiter
from core.settings import TIMES
from utils.auth import request
from utils.utils import paginate

router = APIRouter()


@router.post(
    "/light",
    summary='创建光照信息',
    tags=["light"]
)
@limiter.limit("%d/minute" %TIMES)
async def create_light(request: Request, light_create_model: Lights_Pydantic):
    user = request.state.user
    assert not await Lights.filter(Q(company_id=user.company_id) | Q(system_data=1), name=light_create_model.name,
                                   invalid=0).count(), '光照信息已存在'
    light = Lights(**light_create_model.dict())
    light.user_id = user.id
    light.company_id = user.company_id
    await light.save()
    return light


@router.delete("/light",
               summary='删除光照',
               tags=["light"],
               dependencies=[Depends(AuthorityRole('admin'))])
@limiter.limit("%d/minute" %TIMES)
async def delete_light(request: Request, light_ids: List[int] = Body(..., embed=True)):
    user = request.state.user
    lights = await Lights.filter(Q(company_id=user.company_id) | Q(system_data=1), id__in=light_ids, invalid=0).all()
    assert len(lights) == len(light_ids), '存在错误的光照id'
    for light in lights:
        assert not light.system_data, '系统内置光照参数不能删除'
        light.invalid = light.id
    await Lights.bulk_update(lights, fields=["invalid"])
    return


@router.put(
    "/light/{light_id}",
    summary='更新光照信息',
    tags=["light"]
)
@limiter.limit("%d/minute" %TIMES)
async def update_light(request: Request, light_id: int, light_update_model: Lights_Pydantic):
    user = request.state.user
    light_info = await Lights.filter(Q(company_id=user.company_id) | Q(system_data=1),
                                     id=light_id, invalid=0).first()
    assert light_info, '光照信息不存在'
    assert not light_info.system_data, '系统内置光照参数不可更改'
    if light_info.name != light_update_model.name:
        assert not await Lights.filter(Q(company_id=user.company_id) | Q(system_data=1),
                                     name=light_update_model.name, invalid=0).first(), '光照名称已存在，请更换'
    await light_info.update_from_dict(light_update_model.dict()).save()
    return light_info


@router.get(
    "/light/{light_id}",
    summary='查找指定ID对应光照信息',
    tags=["light"]
)
async def find_specified_light(light_id: int):
    user = request.state.user
    light_info = await Lights.filter(Q(company_id=user.company_id) | Q(system_data=1),
                                     id=light_id, invalid=0).first()
    assert light_info, '光照信息不存在'
    return light_info


@router.get(
    "/light",
    summary='查找所有的光照信息',
    tags=["light"]
)
async def find_all_light(content: str = '', pagesize: int = 15, pagenum: int = 1):
    user = request.state.user
    light_model = Lights.filter(Q(company_id=user.company_id) | Q(system_data=1), invalid=0)
    if content:
        light_model = light_model.filter(Q(name__contains=content) | Q(desc__contains=content))

    total_num = await light_model.count()
    if pagesize == 0:
        data = await light_model.all()
    else:
        data = await light_model.limit(pagesize).offset(max(0, pagenum - 1) * pagesize).all()
    pageinfo = paginate(total_num, pagesize)
    data = sorted(data, key=lambda v: v.modified_at, reverse=True)
    return {"pageinfo": pageinfo, "datas": data}
