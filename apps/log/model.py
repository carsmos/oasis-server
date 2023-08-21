from core.model import fields
from core.model import AbstractBaseModel, TimestampMixin


class Logs(TimestampMixin, AbstractBaseModel):
    logger = fields.CharField(max_length=20)
    msg = fields.TextField(max_length=1024)
    log_level = fields.CharField(max_length=10)
    task_id = fields.IntField()
    type = fields.CharField(max_length=45)
    ip = fields.CharField(max_length=20)
    log_time = fields.DatetimeField(default=None)
    game_time = fields.CharField(max_length=45)

    class Meta:
        table = "logs"
        table_description = "日志表"
        ordering = ["-id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid']
