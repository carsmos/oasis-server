import json

from fastapi import FastAPI, Request, Response, HTTPException
from utils.response_code import ResultResponse, HttpStatus
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)


class aiwrap:
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value


def register_hook(app: FastAPI) -> None:
    """
    请求响应拦截 hook
    :param app:
    :return:
    """

    # 添加登录验证中间件
    @app.middleware("http")
    async def check(request: Request, call_next):
        response: Response = await call_next(request)

        resp_body = [section async for section in response.__dict__['body_iterator']]
        # Repairing FastAPI response
        response.__setattr__('body_iterator', aiwrap(resp_body))

        # Formatting response body for logging
        try:
            resp_body = json.loads(resp_body[0].decode())
        except:
            resp_body = str(resp_body)

        if isinstance(resp_body, dict) and all([k in ['code', 'message', 'result'] for k in resp_body.keys()]):
            return response
        elif response.status_code >= 400:
            return JSONResponse(
                content={"code": response.status_code, "message": resp_body.get('detail', ''), "result": None})
        else:
            return response


def add_limit(app):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)