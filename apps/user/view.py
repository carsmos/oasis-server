import datetime
import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, Body, Request
from fastapi.encoders import jsonable_encoder
from tortoise import transactions

from apps.auth.auth_casbin import Authority, get_casbin, AuthorityRole
from apps.auth.schema import AddUser
from apps.user.model import Users
from core.middleware import limiter
from utils.auth import request
from utils.utils import get_password_hash, paginate, rsa_decode

router = APIRouter()


@router.get(
    "/me",
    summary='获取用户',
    tags=["users"]
)
async def me():
    user = jsonable_encoder(request.state.user)
    del user['password']
    # e = await get_casbin()
    # role = await e.get_roles_for_user(user['username'])
    # print("role", role)
    # user['role'] = role[0] if role else 'member'
    user['role'] = 'admin'
    user_type = "company" if os.getenv('SERVER_TYPE') == 'professional' else "taste"
    user['user_type'] = user_type
    return user


@router.get(
    "/{user_id}",
    summary='获取用户信息',
    tags=["users"],
    dependencies=[Depends(Authority('user,get'))]
)
async def user_info(user_id: str):
    info = await Users.filter(user_id=user_id, invalid=0).first()
    assert info, '用户不存在'
    info = jsonable_encoder(info)
    del info['password']
    return info


@router.delete("/delete_user",
               summary='删除用户',
               tags=["users"],
               dependencies=[Depends(AuthorityRole('admin'))])
@limiter.limit("5/minute")
async def delete_user(request: Request, ids: List[str] = Body(..., embed=True)):
    async with transactions.in_transaction():
        users = await Users.filter(user_id__in=ids, invalid=0).all()
        assert users, '用户不存在'
        e = await get_casbin()
        for user in users:
            role = await e.get_roles_for_user(user.username)
            if role:
                res = await e.delete_roles_for_user(user.username)
                assert res, '删除当前角色失败'
            await user.delete()
    return "ok"


# @router.post('/add_role',
#              summary='添加角色',
#              name='添加角色')
# async def add_role(role: model.RoleOut):
#     role = Role(**role.dict())
#     e = await get_casbin()
#     roles = await e.get_roles_for_user(d.username)
#     await role.save()
#     return role


# @router.post("/add_role_perm",
#              summary="添加角色权限",
#              description="添加角色权限")
# async def add_role_perm(perm_info: RolePerm):
#     role = await Role.get(name=perm_info.role)
#     assert role, '角色不存在'
#
#     e = await get_casbin()
#     res = await e.add_permission_for_role(perm_info.role, perm_info.model, perm_info.act)
#     assert res, '添加角色权限失败，权限已存在'
#     return '添加角色权限成功'


# @router.post('/del_role_perm',
#              summary='删除角色权限',
#              description='删除角色权限')
# async def del_role_perm(perm_info: RolePerm):
#     e = await get_casbin()
#     res = await e.remove_permission_for_role(perm_info.role, perm_info.model, perm_info.act)
#     assert res, '角色权限不存在'
#     return '删除角色权限成功'


# @router.post("/add_user_role",
#              summary="添加用户角色",
#              description="添加用户角色",
#              dependencies=[Depends(AuthorityRole('admin'))])
# async def add_user_role(user_role: UserRole):
#     user = await Users.get(id=user_role.id)
#     assert user, '添加权限的用户不存在，请检查用户名'
#     role = await Role.filter(name=user_role.role).first()
#     assert not role, '角色已存在'
#     e = await get_casbin()
#     await e.delete_roles_for_user(user.username)
#     res = await e.add_role_for_user(user.username, user_role.role)
#     assert res, '添加用户角色失败'
#     return '添加用户角色成功'


@router.post("/mod_user_role",
             summary="角色修改",
             description="角色修改",
             dependencies=[Depends(AuthorityRole('admin'))])
async def mod_role(add_user: AddUser):
    assert await Users.exists(username=add_user.username, invalid=0), '用户不存在'
    assert os.getenv('SERVER_TYPE') == 'professional', "体验版不能修改用户角色"
    assert add_user.role in ['member', 'admin'], '角色类型错误'
    if add_user.password:
        ori_user = await Users.filter(username=add_user.username, invalid=0).first()
        assert ori_user, '用户不已存在'
        try:
            password = rsa_decode(add_user.password)
        except Exception as e:
            assert False, '密码校验失败'
        # assert not verify_password(add_user.password, ori_user.password), '新密码与原密码一致，请重新设置'
        ori_user.password = get_password_hash(password)
        await ori_user.save()
    e = await get_casbin()
    # 1、删除现有角色
    role = await e.get_roles_for_user(add_user.username)
    if role:
        res = await e.delete_roles_for_user(add_user.username)
        assert res, '删除当前角色失败'
    # 添加新角色
    res = await e.add_role_for_user(add_user.username, add_user.role)
    assert res, '添加用户角色失败'
    if add_user.last_day:
        ori_user = await Users.filter(username=add_user.username, invalid=0).first()
        assert ori_user, '用户不已存在'
        ori_user.last_day = add_user.last_day
        await ori_user.save()
    return '修改成功'


@router.post("/add_user",
             summary="添加用户",
             description="添加用户",
             dependencies=[Depends(AuthorityRole('admin'))])
@limiter.limit("5/minute")
async def add_user(request: Request, add_user: AddUser):
    admin_user = request.state.user
    assert not await Users.exists(username=add_user.username, invalid=0), '用户已存在'
    assert os.getenv('SERVER_TYPE') == 'professional', "体验版不能添加用户"
    assert add_user.role in ['member', 'admin'], '角色类型错误'

    e = await get_casbin()
    # 1、删除现有角色
    role = await e.get_roles_for_user(add_user.username)
    if role:
        res = await e.delete_roles_for_user(add_user.username)
        assert res, '删除当前角色失败'
    # 2、添加角色
    res = await e.add_role_for_user(add_user.username, add_user.role)
    assert res, '添加用户角色失败'
    try:
        password = rsa_decode(add_user.password)
    except Exception as e:
        assert False, '密码校验失败'
    user = Users(**add_user.dict())
    user.password = get_password_hash(password)
    user.company_id = admin_user.company_id
    # 用户添加uuid
    user.user_id = str(uuid.uuid1()).replace("-", "")
    await user.save()
    return user


# @router.get('/roles/{user_id}',
#             summary='获取用户角色列表',
#             description='获取用户角色列表')
# async def get_role_list(user_id: int):
#     user_info = await Users.filter(id=user_id, invalid=0).first()
#     assert user_info, '用户不存在'
#     e = await get_casbin()
#     result = await e.get_roles_for_user(user_info.username)
#     return result


@router.post('/all_users',
             summary='获取用户列表',
             description='获取用户列表')
async def get_user_list(content: str = "", pagenum: int = 1, pagesize: int = 15):
    if content:
        user_model = Users.filter(invalid=0, username__contains=content, company_id=request.state.user.company_id)
    else:
        user_model = Users.filter(invalid=0, company_id=request.state.user.company_id)
    total_num = await user_model.count()
    data = await user_model.limit(pagesize).offset(max(0, pagenum - 1) * pagesize).all()
    pageinfo = paginate(total_num, pagesize)
    e = await get_casbin()
    res = []
    for user in data:
        json_user = jsonable_encoder(user)
        roles = await e.get_roles_for_user(user.username)
        role = roles[0] if roles else "member"
        json_user["role"] = role
        now_day = datetime.datetime.now().date()
        timedel = user.last_day - now_day if user.last_day else ""
        life_time = timedel.days if timedel else 0
        json_user['life_time'] = life_time
        del json_user['password']
        res.append(json_user)
    return {"pageinfo": pageinfo, "datas": res}
