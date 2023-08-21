import datetime

from pydantic import BaseModel, Field
from apps.user.model import UserBase


class Token(BaseModel):
    token: str = Field(..., description='Token值')
    token_type: str = Field(..., description='Token类型')


# class UserCreate(BaseModel):
#     username: str = Field(..., description='用户名称')
#     # nickname: str = Field(..., description='昵称')
#     # email: str = Field(..., description='邮箱')
#     is_super: int = Field(..., description='是否超级用户  1是，0不是')# smallint 类型，值为1和0
#     password: str = Field(..., description='密码')
#     company_id: int = Field(..., description="企业id")
#     last_day: datetime.date = Field(None, description='授权日期')
#     category: int = Field(..., description='用户类别： 1为企业版用户，0为体验版用户')
#     role: str = Field(None, description='用户角色： member，admin， super_admin')
#
#     class PydanticMeta:
#         exclude = ["password"]


class UserUpdate(BaseModel):
    username: str = Field(..., description='用户名称')
    oripassword: str = Field(..., description='密码')
    newpassword: str = Field(..., description='密码')

    class PydanticMeta:
        exclude = ["password"]


class AddUser(BaseModel):
    username: str = Field(..., description='用户名称')
    password: str = Field(..., description='密码')
    role: str = Field(..., description='角色')
    last_day: datetime.date = Field(None, description='授权日期')

    class PydanticMeta:
        exclude = ["password"]