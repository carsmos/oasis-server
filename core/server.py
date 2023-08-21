import os
import traceback
import redis as redis

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from utils.auth import OAuth2CustomJwt
from .middleware import register_hook, add_limit
from utils import custom_exc
from utils.response_code import ResultResponse, HttpStatus
from utils.logger import logger
from core import settings, database
from .router import api_router
from aioredis import Redis


def create_app() -> FastAPI:
    """
    生成FatAPI对象
    :return:
    """
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        dependencies=[Depends(OAuth2CustomJwt(tokenUrl="/auth/login"))]
    )

    # 跨域设置
    register_cors(app)

    # 注册路由
    register_router(app)

    # 注册捕获全局异常
    register_exception(app)

    # 初始化
    register_init(app)

    # 请求拦截
    register_hook(app)

    # 添加限流
    add_limit(app)
    return app


def register_router(app: FastAPI) -> None:
    """
    注册路由
    :param app:
    :return:
    """
    # 项目API
    app.include_router(api_router)


def register_cors(app: FastAPI) -> None:
    """
    支持跨域
    :param app:
    :return:
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_exception(app: FastAPI) -> None:
    """
    全局异常捕获
    注意 别手误多敲一个s
    exception_handler
    exception_handlers
    两者有区别
        如果只捕获一个异常 启动会报错
        @exception_handlers(UserNotFound)
    TypeError: 'dict' object is not callable
    :param app:
    :return:
    """

    # 自定义异常 捕获
    @app.exception_handler(custom_exc.TokenExpired)
    async def token_expire_exception_handler(request: Request, exc: custom_exc.TokenExpired):
        """
        token过期
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"token未知用户\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(content=ResultResponse[str](code=HttpStatus.HTTP_420_TOKEN_EXCEPT,
                                                        message='Token 已过期，请重新登录',
                                                        en='Token has expired, please log in again').dict())

    @app.exception_handler(custom_exc.TokenAuthError)
    async def token_auth_exception_handler(request: Request, exc: custom_exc.TokenAuthError):
        """
        用户token异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"用户认证异常\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(
            content=ResultResponse[str](code=HttpStatus.HTTP_418_AUTH_EXCEPT, message='用户认证异常，请重新登录',
                                        en='User authentication is abnormal, please log in again').dict())

    @app.exception_handler(custom_exc.AuthenticationError)
    async def authentication_exception_handler(request: Request, exc: custom_exc.AuthenticationError):
        """
        用户权限不足
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"用户权限不足 \nURL:{request.method}{request.url}")
        return JSONResponse(
            content=ResultResponse[str](code=HttpStatus.HTTP_425_AUTHENTICATION_EXCEPT, message='用户权限不足',
                                        en='Insufficient user rights').dict())

    @app.exception_handler(AssertionError)
    async def inner_validation_exception_handler(request: Request, exc: AssertionError):
        """
        内部业务逻辑异常
        :param request:
        :param exc:
        :return:
        """
        exc = exc.args[0]
        if isinstance(exc, list):
            exc = ','.join(exc)
        from chinese_to_english import to_english
        err_msg = to_english.get(exc, exc)
        return JSONResponse(
            content=ResultResponse[str](code=HttpStatus.HTTP_421_INNER_PARAM_EXCEPT, message=exc, en=err_msg).dict())

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        请求参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"请求参数格式错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(
            content=ResultResponse[str](code=HttpStatus.HTTP_422_QUERY_PARAM_EXCEPT, message='请求参数校验异常',
                                        en='Request parameter validation exception').dict())

    # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        全局所有异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"全局异常\n{request.method}URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}\n")
        return JSONResponse(
            content=ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='服务器异常',
                                        en='server exception').dict())


def register_init(app: FastAPI) -> None:
    """
    初始化连接
    :param app:
    :return:
    """

    @app.on_event("startup")
    async def init_connect():
        # 连接数据库
        await database.init(app)
        logger.info("start server and register_tortoise")
        app.state.redis = await Redis(host=os.environ.get('REDIS_HOST'), db=1, password=os.environ.get('REDIS_PORT'))
        logger.info("start redis")

    @app.on_event('shutdown')
    async def shutdown_connect():
        """
        关闭
        :return:
        """
        logger.info('stop server')
