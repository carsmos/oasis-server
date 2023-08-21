import datetime

from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from core import settings
from apps.user.model import Users, UserBase
from utils.auth import create_access_token
from utils import logger
from utils.utils import verify_password, get_password_hash, validate_email_and_pw, rsa_decode
from datetime import timedelta
from . import schema
from .auth_casbin import get_casbin
from utils.auth import request

router = APIRouter()


@router.post("/jwt/login",
             summary="用户登录认证"
             )
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    通过用户名和密码登录获取 token 值
    :param form_data:
    :return:
    """
    # 验证用户
    user = await Users.get_or_none(username=form_data.username, invalid=0)
    assert user, '用户名或密码错误'

    try:
        password = rsa_decode(form_data.password)
    except Exception as e:
        assert False, '密码校验失败'

    # 验证密码
    assert verify_password(password, user.password), '用户名或密码错误'

    # 登录成功后返回token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.username, expires_delta=access_token_expires, code='')
    response.headers['Authorization'] = 'bearer ' + access_token
    now_day = datetime.datetime.now().date()
    timedel = user.last_day - now_day if user.last_day else ""
    life_time = timedel.days if timedel else 0
    return {'token': access_token, 'token_type': 'bearer', "life_time": life_time,
            "last_day": user.last_day if user.last_day else now_day}


# @router.post('/register',
#              summary='用户注册',
#              response_model=UserBase)
# async def register(adduser: schema.UserCreate):
#     res, reason = validate_email_and_pw(adduser.username, adduser.password)
#     assert res, reason
#     assert not await Users.exists(username=adduser.username, invalid=0), '用户已存在'
#
#     user = Users(**adduser.dict())
#     user.password = get_password_hash(adduser.password)
#     # 用户添加uuid
#     user.user_id = str(uuid.uuid1()).replace("-","")
#     e = await get_casbin()
#     # 1、删除现有角色
#     role = await e.get_roles_for_user(adduser.username)
#     if role:
#         res = await e.delete_roles_for_user(adduser.username)
#         assert res, '删除当前角色失败'
#     # 添加新角色
#     res = await e.add_role_for_user(adduser.username, adduser.role)
#     assert res, '添加用户角色失败'
#     users = await Users.filter(invalid=0, company_id=adduser.company_id, is_super=True).all()
#     await user.save()
#     if not users:
#         await seed_data(user)
#     return user


@router.post('/mod_password',
             summary='修改密码')
async def mod_password(user: schema.UserUpdate):
    ori_user = await Users.filter(username=user.username, invalid=0).first()
    assert ori_user, '用户不存在'

    try:
        oripassword = rsa_decode(user.oripassword)
        newpassword = rsa_decode(user.newpassword)
    except Exception as e:
        assert False, '密码校验失败'

    assert verify_password(oripassword, newpassword), '用户名或密码错误'
    ori_user.password = get_password_hash(newpassword)
    await ori_user.save()
    return "修改成功"
