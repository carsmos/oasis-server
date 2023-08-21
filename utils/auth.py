from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Request, HTTPException, status
from fastapi.security.oauth2 import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from starlette.authentication import AuthenticationError
from pydantic import ValidationError
from fastapi.security.utils import get_authorization_scheme_param
from starlette.responses import JSONResponse

from core import settings
from apps.user.model import Users
from utils import custom_exc

from contextvars import ContextVar

from utils.response_code import ResultResponse, HttpStatus


def bind_contextvar(contextvar):
    class ContextVarBind:
        __slots__ = ()

        def __getattr__(self, name):
            return getattr(contextvar.get(), name)

        def __setattr__(self, name, value):
            setattr(contextvar.get(), name, value)

        def __delattr__(self, name):
            delattr(contextvar.get(), name)

        def __getitem__(self, index):
            return contextvar.get()[index]

        def __setitem__(self, index, value):
            contextvar.get()[index] = value

        def __delitem__(self, index):
            del contextvar.get()[index]

    return ContextVarBind()


request_var: ContextVar[Request] = ContextVar("request")
request: Request = bind_contextvar(request_var)


class OAuth2CustomJwt(OAuth2):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            description: Optional[str] = None,
            auto_error: bool = True,
    ):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        for url, op in settings.NO_VERIFY_URL.items():
            if op == 'eq' and url == request.url.path.lower():
                return None
            elif op == 'in' and url in request.url.path.lower():
                return None

        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None

        try:
            playload = jwt.decode(
                param,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        except (ValidationError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
            )

        username = playload.get('username')
        # username = 'oasis'
        user = await Users.filter(username=username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
            )

        """在 Request 对象中设置用户对象"""

        request.state.user = user
        request_var.set(request)


def create_access_token(
        subject: str,
        code: str,
        expires_delta: timedelta = None
) -> str:
    """
    生成token
    :param subject:需要存储到token的数据
    :param expires_delta:
    :return:
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode = {"exp": expire, "username": subject, "code": code}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
