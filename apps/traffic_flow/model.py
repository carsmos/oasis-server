
from core.model import fields
from core.model import AbstractBaseModel, TimestampMixin

class TrafficFlow(TimestampMixin, AbstractBaseModel):
    actor = fields.CharField(max_length=64)
    actor_class = fields.CharField(max_length=128)


    class Meta:
        table = "traffic_flow"
        table_description = "交通流"
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid', 'password']