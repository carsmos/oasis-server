import utils.utils

from fastapi import APIRouter, status, Body, Depends, Request
from tortoise.expressions import Q
from core.settings import TIMES
from apps.auth.auth_casbin import AuthorityRole
from apps.car.model import Cars
from apps.dynamic.model import Dynamics, Dynamics_Pydantic
from apps.dynamic.schema import DynamicModel
from core.middleware import limiter
from utils.auth import request

router = APIRouter()


@router.post(
    "/dynamics",
    summary='创建动力学模型',
    tags=["Dynamics"]
)
@limiter.limit("%d/minute" %TIMES)
async def create_dynamics(request: Request, dynamic: DynamicModel):
    user = request.state.user
    assert not await Dynamics.filter(Q(company_id=user.company_id) | Q(system_data=1), name=dynamic.name,
                                     invalid=0).first(), '动力学模型名称已存在'
    dynamic = Dynamics(**dynamic.dict())
    dynamic.user_id = user.id
    dynamic.company_id = user.company_id
    await dynamic.save()
    return dynamic


@router.delete(
    "/dynamics/{dynamics_id}",
    summary='删除动力学模型',
    tags=["Dynamics"],
    dependencies=[Depends(AuthorityRole('admin'))]
)
@limiter.limit("%d/minute" %TIMES)
async def delete_dynamics(request: Request, dynamics_id: int, real_exec: int = Body(0, embed=True),
                          cars: dict = Body({}, embed=True)):
    user = request.state.user
    dynamic_info = await Dynamics.filter(Q(company_id=user.company_id) | Q(system_data=1),
                                         id=dynamics_id, invalid=0).first()
    assert dynamic_info, '动力学模型不存在'
    assert not dynamic_info.system_data, '系统动力学模型不能删除'

    car_list = await Cars.filter(company_id=user.company_id, invalid=0, dynamics_id=dynamics_id).all()
    if real_exec == 0:
        return car_list
    else:
        assert len(cars) == len(car_list), '存在未处理的主车信息'
    for c in car_list:
        car = cars.get(str(c.id), {})
        if car['action'] == 'replace':
            c.dynamics_id = car['dynamics_id']
            await c.save()
    dynamic_info.invalid = dynamics_id
    res = await dynamic_info.save()
    return res


@router.put(
    "/dynamics/{dynamics_id}",
    summary='更改系统动力学模型',
    tags=["Dynamics"]
)
@limiter.limit("%d/minute" %TIMES)
async def update_dynamics(request: Request, dynamics_id: int, dynamic: DynamicModel):
    user = request.state.user
    dynamic_info = await Dynamics.filter(Q(company_id=user.company_id) | Q(system_data=1),
                                         id=dynamics_id, invalid=0).first()
    assert dynamic_info, '动力学模型不存在'
    assert not dynamic_info.system_data, '系统动力学模型不可更改'
    if dynamic_info.name != dynamic.name:
        assert not await Dynamics.filter(Q(company_id=user.company_id) | Q(system_data=1), name=dynamic.name,
                                         invalid=0), '动力学模型名称已存在，请更换'
    await dynamic_info.update_from_dict(dynamic.dict(include={"name", "desc", "param"})).save()
    return dynamic_info


@router.get(
    "/dynamics/{dynamics_id}",
    summary='获取动力学模型',
    tags=["Dynamics"]
)
async def get_dynamics(dynamics_id: int):
    user = request.state.user
    dynamic = await Dynamics.filter(Q(company_id=user.company_id) | Q(system_data=1),
                                    id=dynamics_id, invalid=0).first()
    assert dynamic, "动力学模型不存在"
    return dynamic


@router.get(
    "/dynamics",
    summary='展示动力学模型',
    tags=["Dynamics"]
)
async def list_dynamics(content: str = "", pagesize: int = 15, pagenum: int = 1):
    user = request.state.user
    dynamic_model = Dynamics.filter(Q(company_id=user.company_id) | Q(system_data=1), invalid=0)
    if content:
        dynamic_model = dynamic_model.filter(Q(name__contains=content) | Q(desc__contains=content))

    total_num = await dynamic_model.count()
    if pagesize == 0:
        res = await dynamic_model.all()
    else:
        res = await dynamic_model.limit(pagesize).offset(max(0, pagenum - 1) * pagesize).all()
    pageinfo = utils.utils.paginate(total_num, pagesize)
    res = sorted(res, key=lambda v: v.modified_at, reverse=True)
    return {'pageinfo': pageinfo, 'datas': res}
