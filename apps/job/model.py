from core.model import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from core.model import AbstractBaseModel, TimestampMixin
from pydantic.typing import List, Optional


class Jobs(TimestampMixin, AbstractBaseModel):
    name = fields.CharField(max_length=64)
    name_en = fields.CharField(max_length=64, null=True)
    user_id = fields.IntField()
    desc_en = fields.CharField(max_length=256, null=True)
    desc = fields.CharField(max_length=256, null=True)
    status = fields.CharField(max_length=10)
    render_mode = fields.CharField(max_length=10)
    controller = fields.CharField(max_length=32)
    controller_version = fields.CharField(max_length=50)
    scenario_ids = fields.JSONField()
    car_id = fields.IntField()
    start_time = fields.DatetimeField(null=True)
    end_time = fields.DatetimeField(null=True)
    car_snap = fields.JSONField(default={}, null=True)
    sensors_snap = fields.JSONField(default={}, null=True)
    system_data = fields.BooleanField(default=False)
    company_id = fields.IntField(default=1)
    view_record = fields.BooleanField(default=False)
    show_game_window = fields.BooleanField(default=False)

    class Meta:
        table = "jobs"
        table_description = "作业"
        ordering = ["-created_at", "id"]
        unique_together = (("invalid", "name", "user_id", 'company_id'),)
        indexes = (("user_id", "status", "invalid"),)

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid']


Jobs_Pydantic = pydantic_model_creator(Jobs, name="Jobs")
JobsIn_Pydantic = pydantic_model_creator(Jobs, name="JobsIn", exclude_readonly=True)
