from core.model import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from core.model import AbstractBaseModel, TimestampMixin


class Sensors(TimestampMixin, AbstractBaseModel):
    name = fields.CharField(max_length=64)
    name_en = fields.CharField(max_length=64, null=True)
    user_id = fields.IntField()
    desc = fields.CharField(max_length=64, null=True)
    desc_en = fields.CharField(max_length=64, null=True)
    type = fields.CharField(max_length=64, null=False)
    group_type = fields.CharField(max_length=64, null=False)
    param = fields.JSONField()
    system_data = fields.BooleanField(default=False)
    company_id = fields.IntField(default=1)

    class Meta:
        table = "sensors"
        table_description = "传感器表"
        ordering = ["-created_at", "id"]
        unique_together = (("invalid", "name", "user_id", 'company_id'),)

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid']


Sensors_Pydantic = pydantic_model_creator(Sensors, name="Sensor")
SensorsIn_Pydantic = pydantic_model_creator(Sensors, name="SensorIn", exclude_readonly=True)


class SensorData(TimestampMixin, AbstractBaseModel):
    task_id = fields.IntField()
    sensor_type = fields.CharField(max_length=64)
    sensor_name = fields.CharField(max_length=64)
    car_sensor_id = fields.IntField()
    process_rate_img = fields.IntField(null=True)
    process_rate_video = fields.IntField(null=True)
    process_rate_data = fields.IntField(null=True)
    process_rate_semantic = fields.IntField(null=True)
    process_rate_instance = fields.IntField(null=True)
    data_url = fields.CharField(max_length=256, null=True)
    platform = fields.CharField(max_length=20, null=True)
    data_size = fields.CharField(max_length=20, null=True)
    cam_url = fields.CharField(max_length=256, null=True)
    process_rate_cam = fields.IntField(null=True)
    system_data = fields.BooleanField(default=False)
    company_id = fields.IntField(default=1)

    class Meta:
        table = "sensor_data"
        table_description = "传感器数据表"
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid']


SensorData_Pydantic = pydantic_model_creator(SensorData, name="SensorData")
SensorDataIn_Pydantic = pydantic_model_creator(SensorData, name="SensorDataIn", exclude_readonly=True)
