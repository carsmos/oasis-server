from tortoise import models
from core.model import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from core.model import AbstractBaseModel, TimestampMixin


class Controllers(TimestampMixin, AbstractBaseModel):
    name = fields.CharField(max_length=64, null=True)
    user_id = fields.IntField()
    parent_id = fields.IntField(default=0)
    desc = fields.CharField(max_length=64, null=True)
    company_id = fields.IntField(default=1)
    type = fields.CharField(max_length=64)
    version = fields.CharField(max_length=30, null=True)
    setup_file_name = fields.CharField(max_length=60, null=True)
    config_file_name = fields.CharField(max_length=60, null=True)
    data_flow_file_name = fields.CharField(max_length=64, null=True)

    class Meta:
        table = "controllers"
        table_description = "车辆控制系统表"
        ordering = ["-created_at", "id"]
        unique_together = (("invalid", "company_id", "id"),)

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid']


Controller_Pydantic = pydantic_model_creator(Controllers, name="Controller")
ControllerIn_Pydantic = pydantic_model_creator(Controllers, name="ControllerIn", exclude_readonly=True)
