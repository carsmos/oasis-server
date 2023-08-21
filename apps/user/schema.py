# 角色权限
from pydantic import BaseModel, Field


class RolePerm(BaseModel):
    role: str = Field(..., description='角色')
    model: str = Field(..., description='模块')
    act: str = Field(..., description='权限行为')

    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'role': 'guest',
                'model': 'auth',
                'act': 'add'
            }
        }


# 用户权限配置
class UserPerm(BaseModel):
    user: str = Field(..., description='用户名')
    model: str = Field(..., description='模块')
    act: str = Field(..., description='权限行为')

    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'user': 'zhangsan',
                'model': 'user',
                'act': 'add'
            }
        }


# 用户角色配置
class UserRole(BaseModel):
    id: int = Field(..., description='用户id')
    role: str = Field(..., description='角色')

    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'id': 1,
                'role': 'guest'
            }
        }

class User(BaseModel):
    id: int = Field(..., description='用户id')
    role: str = Field(..., description='角色')

    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'id': 1,
                'role': 'guest'
            }
        }