#!/usr/bin/env python
"""
/*******************************************************************************
 * GuardStrike Confidential
 * Copyright (C) 2022 GuardStrike Inc. All rights reserved.
 * The source code for this program is not published
 * and protected by copyright controlled
 *******************************************************************************/
"""

from core.model import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from core.model import AbstractBaseModel, TimestampMixin


class EvaluationCriteria(TimestampMixin, AbstractBaseModel):
    name = fields.CharField(max_length=64)
    name_en = fields.CharField(max_length=64, null=True)
    user_id = fields.IntField()
    desc = fields.CharField(max_length=64, null=True)
    desc_en = fields.CharField(max_length=64, null=True)
    system_data = fields.BooleanField(default=False)
    criteria = fields.JSONField(null=True)
    company_id = fields.IntField(default=1)

    class Meta:
        table = "evaluation_criteria"
        table_description = "评价准则"
        ordering = ["-created_at", "id"]
        unique_together = (("invalid", "name", "user_id", 'company_id'),)

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'invalid', 'user_id']


Criteria_Pydantic = pydantic_model_creator(EvaluationCriteria, name="Criteria")
CriteriaIn_Pydantic = pydantic_model_creator(EvaluationCriteria, name="CriteriaIn", exclude_readonly=True)

