from tortoise.contrib.fastapi import register_tortoise
from typing import Type

from tortoise import Model
from settings import TORTOISE_ORM


class Router:
    @staticmethod
    def db_for_read(model: Type[Model]):
        return "slave"

    @staticmethod
    def db_for_write(model: Type[Model]):
        return "master"


async def init(app):
    # 该方法会在fastapi启动时触发，内部通过传递进去的app对象，监听服务启动和终止事件
    # 当检测到启动事件时，会初始化Tortoise对象，如果generate_schemas为True则还会进行数据库迁移
    # 当检测到终止事件时，会关闭连接
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,  # 如果数据库为空，则自动生成对应表单，生产环境不要开
        # add_exception_handlers=True,  # 生产环境不要开，会泄露调试信息
    )
