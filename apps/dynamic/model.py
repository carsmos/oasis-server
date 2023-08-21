from core.model import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from core.model import AbstractBaseModel, TimestampMixin


class Dynamics(TimestampMixin, AbstractBaseModel):
    name = fields.CharField(max_length=64)
    name_en = fields.CharField(max_length=64, null=True)
    user_id = fields.IntField()
    desc = fields.CharField(max_length=64, null=True)
    desc_en = fields.CharField(max_length=64, null=True)
    param = fields.JSONField()
    system_data = fields.BooleanField(default=False)
    company_id = fields.IntField(default=1)

    class Meta:
        table = "dynamics"
        table_description = "动力学模型"
        ordering = ["-created_at", "id"]
        unique_together = (("invalid", "name", "user_id", 'company_id'),)

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid', 'user_id']


Dynamics_Pydantic = pydantic_model_creator(Dynamics, name="Dynamics")
DynamicsIn_Pydantic = pydantic_model_creator(Dynamics, name="DynamicsIn", exclude_readonly=True)
