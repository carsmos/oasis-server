from core.model import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from core.model import AbstractBaseModel, TimestampMixin


class Scenarios(TimestampMixin, AbstractBaseModel):
    name = fields.CharField(max_length=64)
    name_en = fields.CharField(max_length=64, null=True)
    user_id = fields.IntField()
    desc = fields.CharField(max_length=64, default="", null=True)
    desc_en = fields.CharField(max_length=64, null=True)
    tags = fields.JSONField(null=False, default=[])
    tags_en = fields.JSONField(null=True, default=[])
    type = fields.CharField(max_length=10)
    parent_id = fields.IntField(null=True)
    lever = fields.CharField(null=True, max_length=20)
    map_name = fields.CharField(null=True, max_length=20)
    # map_id = fields.IntField(null=True)
    traffic_flow = fields.JSONField(null=True)
    open_scenario_json = fields.JSONField(null=False, default={})
    ui_entities_json = fields.JSONField(null=True)
    environment = fields.JSONField(null=True)
    evaluation_standard = fields.JSONField(null=True)
    is_temp = fields.BooleanField(default=False)
    system_data = fields.BooleanField(default=False)
    criterion_id = fields.IntField(null=True)
    company_id = fields.IntField(default=1)

    class Meta:
        table = "scenarios"
        table_description = "场景"
        ordering = ["-modified_at", "id"]
        indexes = (("user_id", "is_temp"),)
        unique_together = (("user_id", "invalid", "name", "parent_id", 'company_id'),)

    class PydanticMeta:
        exclude = ['invalid']


Scenarios_Pydantic = pydantic_model_creator(Scenarios, name="Scenarios")
ScenariosIn_Pydantic = pydantic_model_creator(Scenarios, name="ScenariosIn", exclude_readonly=True)


class ScenarioParams(TimestampMixin, AbstractBaseModel):
    scenario_id = fields.IntField()
    item_type = fields.CharField(max_length=10)
    item_key = fields.CharField(max_length=20)
    item_value = fields.JSONField(null=False)

    class Meta:
        table = "scenarioparams"
        table_description = "场景参数"
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid']


ScenarioParams_Pydantic = pydantic_model_creator(ScenarioParams, name="ScenarioParams")
ScenarioParamsIn_Pydantic = pydantic_model_creator(ScenarioParams, name="ScenarioParamsIn", exclude_readonly=True)
