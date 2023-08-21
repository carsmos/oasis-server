from core.model import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from core.model import AbstractBaseModel, TimestampMixin


class Lights(TimestampMixin, AbstractBaseModel):
    name = fields.CharField(max_length=64)
    name_en = fields.CharField(max_length=64, null=True)
    user_id = fields.IntField()
    desc = fields.CharField(max_length=64, null=True)
    desc_en = fields.CharField(max_length=64, null=True)
    sun_azimuth_angle = fields.FloatField()
    sun_altitude_angle = fields.FloatField()
    system_data = fields.BooleanField(default=False)
    company_id = fields.IntField(default=1)

    class Meta:
        table = "lights"
        table_description = "光照"
        ordering = ["-created_at", "id"]
        unique_together = (("invalid", "name", "user_id", 'company_id'),)

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid', 'user_id']


Lights_Pydantic = pydantic_model_creator(Lights, name="Lights")
LightsIn_Pydantic = pydantic_model_creator(Lights, name="LightsIn", exclude_readonly=True)
