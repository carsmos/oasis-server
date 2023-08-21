from tortoise import models
from core.model import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from core.model import AbstractBaseModel, TimestampMixin


class Cars(TimestampMixin, AbstractBaseModel):
    name = fields.CharField(max_length=64)
    name_en = fields.CharField(max_length=64, null=True)
    user_id = fields.IntField()
    desc = fields.CharField(max_length=64, null=True)
    desc_en = fields.CharField(max_length=64, null=True)
    vehicle_color = fields.CharField(max_length=64, null=False)
    light_state = fields.CharField(max_length=20, null=True)
    type = fields.CharField(max_length=64, null=False)
    dynamics_id = fields.IntField()
    render_mode = fields.CharField(max_length=20, null=True)
    system_data = fields.BooleanField(default=False)
    company_id = fields.IntField(default=1)

    class Meta:
        table = "cars"
        table_description = "车辆表"
        ordering = ["-created_at", "id"]
        unique_together = (("invalid", "name", "user_id"),)

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid']


Cars_Pydantic = pydantic_model_creator(Cars, name="Car")
CarsIn_Pydantic = pydantic_model_creator(Cars, name="CarIn", exclude_readonly=True)


class CarSensors(TimestampMixin, AbstractBaseModel):
    car_id = fields.IntField()
    sensor_id = fields.IntField()
    name = fields.CharField(max_length=64)
    name_en = fields.CharField(max_length=64, null=True)
    nick_name = fields.CharField(max_length=64)
    type = fields.CharField(max_length=64)
    position_x = fields.FloatField()
    position_y = fields.FloatField()
    position_z = fields.FloatField()
    roll = fields.FloatField()
    pitch = fields.FloatField()
    yaw = fields.FloatField()
    system_data = fields.BooleanField(default=False)
    company_id = fields.IntField(default=1)
    data_record = fields.BooleanField(default=False)
    semantic = fields.BooleanField(default=False)
    instance = fields.BooleanField(default=False)

    class Meta:
        table = "carsensors"
        table_description = "车辆传感器位置表"
        ordering = ["-created_at", "id"]
        unique_together = (("invalid", "nick_name", "type", "car_id", "company_id"),)

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid']


CarSensors_Pydantic = pydantic_model_creator(CarSensors, name="CarSensors")
CarSensorsIn_Pydantic = pydantic_model_creator(CarSensors, name="CarSensorsIn", exclude_readonly=True)
