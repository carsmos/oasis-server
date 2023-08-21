from core.model import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from core.model import AbstractBaseModel, TimestampMixin


class Tasks(TimestampMixin, AbstractBaseModel):
    user_id = fields.IntField()
    job_id = fields.IntField()
    job_name = fields.CharField(max_length=64)
    name = fields.CharField(max_length=64)
    desc = fields.CharField(max_length=64)
    scenario_id = fields.IntField()
    scenario_tags = fields.JSONField()
    scenario_param = fields.JSONField(null=True)
    status = fields.CharField(max_length=10, null=True)
    result = fields.JSONField(null=True)
    replay_url = fields.CharField(max_length=256, null=True)
    cam_url = fields.CharField(max_length=256, null=True)
    index = fields.DecimalField(max_digits=64, decimal_places=2, default=0)
    start_time = fields.DatetimeField(null=True)
    end_time = fields.DatetimeField(null=True)
    process_rate = fields.CharField(max_length=10, null=True)
    running_time = fields.CharField(max_length=30, null=True)
    mileage = fields.IntField(null=True)
    ret_status = fields.CharField(max_length=20, null=True)
    system_data = fields.BooleanField(default=False)
    company_id = fields.IntField(default=1)

    class Meta:
        table = "tasks"
        table_description = "任务"
        ordering = ["-created_at", "id"]
        unique_together = (("invalid", "name", "user_id", "job_id", 'company_id', "id"),)
        indexes = (("job_id", "status", "invalid", "user_id"),)

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid']


Tasks_Pydantic = pydantic_model_creator(Tasks, name="Tasks")
TasksIn_Pydantic = pydantic_model_creator(Tasks, name="TasksIn", exclude_readonly=True)
