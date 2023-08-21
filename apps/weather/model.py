from core.model import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from core.model import AbstractBaseModel, TimestampMixin


class Weathers(TimestampMixin, AbstractBaseModel):
    name = fields.CharField(max_length=64)
    name_en = fields.CharField(max_length=64, null=True)
    user_id = fields.IntField()
    desc = fields.CharField(max_length=64, null=True)
    desc_en = fields.CharField(max_length=64, null=True)
    cloudiness = fields.FloatField(max_length=20)
    precipitation = fields.FloatField()
    precipitation_deposits = fields.FloatField(max_length=20)
    wind_intensity = fields.FloatField()
    fog_density = fields.FloatField(max_length=20)
    fog_distance = fields.FloatField(max_length=20)
    wetness = fields.FloatField(max_length=20)
    fog_falloff = fields.FloatField(max_length=20)
    fog_visualrange = fields.FloatField(max_length=20)
    sky_visibility = fields.BooleanField()
    cloudstate = fields.CharField(max_length=20)
    system_data = fields.BooleanField(default=False)
    company_id = fields.IntField(default=1)

    class Meta:
        table = "weather"
        table_description = "天气"
        ordering = ["-created_at", "id"]
        unique_together = (("invalid", "name", "user_id", 'company_id'),)

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid', 'user_id']


Weathers_Pydantic = pydantic_model_creator(Weathers, name="Weathers")
WeathersIn_Pydantic = pydantic_model_creator(Weathers, name="WeathersIn", exclude_readonly=True)
