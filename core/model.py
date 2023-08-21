# -*- coding: utf-8 -*-
"""
@description: 基础模型
"""
import datetime

from tortoise import fields
from tortoise.models import Model


class DatetimeField(fields.DatetimeField):
    """重载日期时间模型字段"""

    def __init__(self, *args, **kwargs):
        super(DatetimeField, self).__init__(*args, **kwargs)

    def to_python_value(self, value: datetime.datetime) -> [str, None]:
        if value is None:
            value = None
        else:
            try:
                value = value.strftime("%Y-%m-%d %H:%M:%S")
                self.validate(value)
            except Exception as ex:
                value = super(DatetimeField, self).to_python_value(value)
        return value


fields.DatetimeField = DatetimeField


class TimestampMixin:
    created_at = fields.DatetimeField(
        null=True, auto_now_add=True, description="创建时间")
    modified_at = fields.DatetimeField(
        null=True, auto_now=True, description="更新时间")


class AbstractBaseModel(Model):
    id = fields.IntField(pk=True)
    invalid = fields.IntField(
        null=False, default=0, description="逻辑删除:0=未删除,id=删除")

    class Meta:
        abstract = True
