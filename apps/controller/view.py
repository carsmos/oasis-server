import utils.utils

from tortoise import transactions
from fastapi import APIRouter, Depends, Request
from apps.auth.auth_casbin import AuthorityRole
from apps.controller.model import Controllers
from core.middleware import limiter
from utils.auth import request
from core.settings import TIMES
from tortoise.expressions import Q
from apps.controller.schema import ControllerModel, VersionModel
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/create_controller",
             summary='创建车辆控制系统',
             tags=["Controllers"])
@limiter.limit("%d/minute" %TIMES)
async def create_controller(request: Request, controller_model: ControllerModel):
    user = request.state.user
    assert not await Controllers.filter(company_id=user.company_id, name=controller_model.name,
                                 invalid=0).first(), '车辆控制系统名称已存在，请更换'
    controller = Controllers(**controller_model.dict())
    controller.user_id = user.id
    controller.company_id = user.company_id
    controller_info = controller.__dict__
    await controller.save()
    return controller_info


@router.post("/create_controller_version",
             summary='创建车辆控制版本',
             tags=["Controllers"])
@limiter.limit("%d/minute" %TIMES)
async def create_version(request: Request, controller_model: VersionModel):
    user = request.state.user
    assert not await Controllers.filter(company_id=user.company_id, version=controller_model.version, invalid=0,
                                        parent_id=controller_model.parent_id).first(), '车辆控制系统版本已存在，请更换'
    controller = Controllers(**controller_model.dict())
    controller.user_id = user.id
    controller.company_id = user.company_id
    controller_info = controller.__dict__
    await controller.save()
    return controller_info


@router.put("/update_controller_version/{controller_id}",
            summary='修改控制系统版本',
            tags=["Controllers"])
@limiter.limit("%d/minute" %TIMES)
async def update_controller_version(request: Request, controller_id, controller_model: VersionModel):
    user = request.state.user
    controller_info = await Controllers.filter(company_id=user.company_id, id=controller_id, invalid=0).first()
    assert controller_info, '车辆控制系统版本不存在'
    if controller_model.version != controller_model.version:
        assert not await Controllers.filter(company_id=user.company_id, version=controller_model.version,
                                            parent_id=controller_model.parent_id, invalid=0).first(), \
                                            '车辆控制系统版本已存在，请更换'
    await controller_info.update_from_dict(controller_model.dict()).save()
    return


@router.put("/update_controller/{controller_id}",
            summary='修改控制系统',
            tags=["Controllers"])
@limiter.limit("%d/minute" %TIMES)
async def update_controller(request: Request, controller_id, controller_model: ControllerModel):
    user = request.state.user
    controller_info = await Controllers.filter(company_id=user.company_id, id=controller_id, invalid=0).first()
    assert controller_info, '车辆控制系统不存在'
    if controller_model.name != controller_model.name:
        assert not await Controllers.filter(company_id=user.company_id, name=controller_model.name,
                                            invalid=0).first(), '车辆控制系统名称已存在，请更换'
    await controller_info.update_from_dict(controller_model.dict()).save()
    return


@router.delete(
    "/delete_controller_version/{version_id}",
    summary='删除车辆控制系统版本',
    tags=["Controllers"],
    dependencies=[Depends(AuthorityRole('admin'))])
@limiter.limit("%d/minute" %TIMES)
async def delete_version(request: Request, version_id: int):
    user = request.state.user
    controller = await Controllers.filter(company_id=user.company_id, id=version_id, invalid=0).first()
    assert controller, '车辆控制系统版本不存在'
    controller.invalid = controller.id
    await controller.save()
    return 'ok'


@router.delete(
    "/delete_controller/{controller_id}",
    summary='删除车辆控制系统',
    tags=["Controllers"],
    dependencies=[Depends(AuthorityRole('admin'))])
@limiter.limit("%d/minute" %TIMES)
async def delete_controller(request: Request, controller_id: int):
    user = request.state.user
    async with transactions.in_transaction():
        controller = await Controllers.filter(company_id=user.company_id, id=controller_id, invalid=0).first()
        assert controller, '车辆控制系统不存在'
        controller.invalid = controller.id
        versions = await Controllers.filter(company_id=user.company_id, parent_id=controller.id, invalid=0).all()
        for version in versions:
            version.invalid = version.id
            await version.save()
        await controller.save()
    return 'ok'


@router.get("/get_controller",
            summary='获取车辆控制系统',
            tags=["Controllers"])
async def get_controller(controller_id: int):
    user = request.state.user
    controller = await Controllers.filter(company_id=user.company_id, id=controller_id, invalid=0).first()
    assert controller, "车辆控制系统不存在"
    controller_versions = await Controllers.filter(parent_id=controller.id, invalid=0).all()
    return {"controller": controller, "version_list": controller_versions}


@router.get(
    "/controllers",
    summary='获取所有车辆控制系统',
    tags=["Controllers"]
)
async def get_all_controllers(pagenum: int = 1, pagesize: int = 0, content: str = ""):
    user = request.state.user
    controllers_model = Controllers.filter(company_id=user.company_id, invalid=0, type='controller').all()
    if content:
        controllers_model = controllers_model.filter(Q(name__contains=content) | Q(desc__contains=content), invalid=0)

    total_num = await controllers_model.count()
    if pagesize == 0:
        res = await controllers_model.all()
    else:
        res = await controllers_model.limit(pagesize).offset(max(0, pagenum - 1) * pagesize).all()
    pageinfo = utils.utils.paginate(total_num, pagesize)

    data = []
    for model in res:
        versions = await Controllers.filter(parent_id=model.id, invalid=0).all()
        model = jsonable_encoder(model)
        model['versions'] = versions
        data.append(model)
    data = sorted(data, key=lambda v: v['modified_at'], reverse=True)
    return {'pageinfo': pageinfo, 'datas': data}
