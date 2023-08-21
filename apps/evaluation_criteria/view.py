#!/usr/bin/env python
"""
/*******************************************************************************
 * GuardStrike Confidential
 * Copyright (C) 2022 GuardStrike Inc. All rights reserved.
 * The source code for this program is not published
 * and protected by copyright controlled
 *******************************************************************************/
"""
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException, Request, Body, Query, Form
from tortoise.expressions import Q

from apps.auth.auth_casbin import AuthorityRole
from apps.evaluation_criteria.model import EvaluationCriteria, Criteria_Pydantic
from apps.scenario.model import Scenarios
from core.middleware import limiter
from core.settings import TIMES
from utils.auth import request
from utils.utils import paginate

router = APIRouter()


@router.post(
    "/evaluation_criteria",
    summary='创建评价准则',
    tags=["criteria"]
)
@limiter.limit("%d/minute" %TIMES)
async def create_criteria(request: Request, criteria_create_model: Criteria_Pydantic):
    user = request.state.user
    assert not await EvaluationCriteria.filter(name=criteria_create_model.name, company_id=user.company_id,
                                               invalid=0).count(), '评价准则已存在'
    criteria = EvaluationCriteria(**criteria_create_model.dict())
    criteria.user_id = user.id
    criteria.company_id = user.company_id
    await criteria.save()
    return criteria


@router.delete("/evaluation_criteria",
               summary='删除评价准则',
               tags=["criteria"],
               dependencies=[Depends(AuthorityRole('admin'))])
@limiter.limit("%d/minute" %TIMES)
async def delete_criteria(request: Request, criteria_ids: List[int] = Body(..., embed=True)):
    user = request.state.user
    criteria = await EvaluationCriteria.filter(id__in=criteria_ids, invalid=0, company_id=user.company_id).all()
    assert len(criteria) == len(criteria_ids), '存在错误评价准则id'
    for criterion in criteria:
        criterion.invalid = criterion.id
        assert not criterion.system_data, '系统评价准则不可删除'
    await EvaluationCriteria.bulk_update(criteria, fields=["invalid"])
    return


@router.delete("/evaluation_criteria/{criteria_id}",
               tags=["criteria"])
@limiter.limit("%d/minute" %TIMES)
async def delete_criteria(request: Request, criteria_id: int, real_exec: int = Body(0, embed=True),
                          scenarios: dict = Body({}, embed=True)):
    user = request.state.user
    criteria = await EvaluationCriteria.filter(id=criteria_id, invalid=0, company_id=user.company_id).first()
    assert criteria, '错误评价准则'
    assert not criteria.system_data, '系统评价准则不可删除'
    scenario_list = await Scenarios.filter(criterion_id=criteria_id, company_id=user.company_id, invalid=0).all()
    if not real_exec:
        return scenario_list
    else:
        assert len(scenario_list) == len(scenarios), '存在未处理的场景信息'

        for s in scenario_list:
            scenario = scenarios.get(str(s.id), {})
            if scenario['action'] == 'replace':
                evaluation_standard = s.evaluation_standard
                evaluation_standard['templateId'] = scenario['criterion_id']
                await Scenarios.filter(id=s.id).update(criterion_id=scenario['criterion_id'],
                                                       evaluation_standard=evaluation_standard)
                # s.criterion_id = scenario['criterion_id']
                # await s.save()
            if scenario['action'] == 'use_default':
                s.evaluation_standard = '{"jerk": {"enabled": true, "JerkLateralTest": 15, "JerkLongitudinalTest": 5}, "velocity": {"enabled": true, "MaxVelocityTest": 120, "MinVelocityTest": 0}, "OnRoadTest": true, "templateId": "", "useTemplate": false, "acceleration": {"enabled": true, "AccelerationLateralTest": 2.3, "AccelerationVerticalTest": 0.15, "AccelerationLongitudinalTest": 6}, "CollisionTest": true, "RunRedLightTest": true, "averageVelocity": {"enabled": false, "MaxAverageVelocityTest": 120, "MinAverageVelocityTest": 10}, "OntoSolidLineTest": true, "DrivenDistanceTest": true, "RoadSpeedLimitTest": true, "ReachDestinationTest": true}'
                s.criterion_id = None
                await s.save()
            if scenario['action'] == 'only_param':
                s.evaluation_standard = criteria.criteria
                s.criterion_id = None
                await s.save()

        criteria.invalid = criteria_id
        await criteria.save()
    return


@router.put(
    "/evaluation_criteria/{criterion_id}",
    summary='更新评价准则',
    tags=["criteria"]
)
@limiter.limit("%d/minute" %TIMES)
async def update_criteria(request: Request, criterion_id: int, criteria_update_model: Criteria_Pydantic):
    user = request.state.user
    criterion_info = await EvaluationCriteria.filter(id=criterion_id, invalid=0, company_id=user.company_id).first()
    assert criterion_info, '评价准则不存在'
    assert not criterion_info.system_data, '系统评价准则不可编辑'
    if criteria_update_model.name != criterion_info.name:
        assert not await EvaluationCriteria.filter(name=criteria_update_model.name, invalid=0,
                                                   company_id=user.company_id).first(), '评价标准名称已存在，请更换'
    await criterion_info.update_from_dict(criteria_update_model.dict()).save()
    criteria = criterion_info.criteria
    criteria['useTemplate'] = True
    criteria['templateId'] = criterion_info.id
    await Scenarios.filter(criterion_id=criterion_info.id, invalid=0,
                           company_id=user.company_id).update(evaluation_standard=criteria)
    return criterion_info


@router.get(
    "/evaluation_criteria/{criterion_id}",
    summary='查找指定的评价准则',
    tags=["criteria"]
)
async def find_specified_criterion(criterion_id: int):
    user = request.state.user
    criterion_info = await EvaluationCriteria.filter(Q(company_id=user.company_id) | Q(system_data=1),
                                                     id=criterion_id, invalid=0).first()
    assert criterion_info, '评价准则不存在'
    return criterion_info


@router.get(
    "/evaluation_criteria",
    summary='查找所有评价准则',
    tags=["criteria"]
)
async def find_all_criteria(content: str = '', pagesize: int = 15, page_num: int = 1):
    user = request.state.user
    criteria_info = EvaluationCriteria.filter(Q(company_id=user.company_id) | Q(system_data=1),
                                              invalid=0)
    if content:
        criteria_info = criteria_info.filter(Q(name__contains=content) | Q(desc__contains=content))

    total_num = await criteria_info.count()
    if pagesize == 0:
        data = await criteria_info.all()
    else:
        data = await criteria_info.limit(pagesize).offset(max(0, page_num - 1) * pagesize).all()
    pageinfo = paginate(total_num, pagesize)
    data = sorted(data, key=lambda v: v.modified_at, reverse=True)
    return {"pageinfo": pageinfo, "datas": data}
