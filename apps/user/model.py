from core.model import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from core.model import AbstractBaseModel, TimestampMixin


class Role(TimestampMixin, AbstractBaseModel):
    name = fields.CharField(max_length=32, unique=True, description='角色名')
    description = fields.CharField(max_length=256, description='角色描述')

    class Meta:
        table = 'roles'
        table_description = '角色表'
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", "invalid"]


RoleCreate = pydantic_model_creator(Role, name='RoleCreate')
RoleOut = pydantic_model_creator(Role, name='RoleOut')


class Users(TimestampMixin, AbstractBaseModel):
    username = fields.CharField(max_length=64)
    nickname = fields.CharField(max_length=128, null=True)
    is_super = fields.SmallIntField(default=0)
    company_id = fields.IntField(default=1)
    mobile = fields.CharField(max_length=15, null=True)
    email = fields.CharField(max_length=64, null=True)
    password = fields.CharField(max_length=128, null=False)
    avatar = fields.CharField(max_length=256, null=True)
    last_day = fields.DateField(null=True, description="授权时间")
    category = fields.SmallIntField(default=1, description="用户类型")
    user_id = fields.CharField(max_length=64)

    class Meta:
        table = "users"
        table_description = "用户表信息"
        ordering = ["-created_at", "id"]
        unique_together = (("company_id", "id"),)

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid', 'password']


UserBase = pydantic_model_creator(Users, name="UserBase")
UserIn = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
