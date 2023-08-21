import collections
import shutil
import copy
import json
import os
import zipfile
import time
from typing import List, Union, Any, Dict

from fastapi import APIRouter, Depends, status, HTTPException, Request, Body, Query, Form, UploadFile, File
from starlette.responses import FileResponse
from tortoise import transactions
from tortoise.expressions import Q
from core.settings import TIMES
from core.middleware import limiter
from .OpenscenarioTool.check_xosc import XoscChecker
from .OpenscenarioTool.outer_xml_to_json import OuterXoscDeserializer
from .OpenscenarioTool.param_generalization import ParamGeneralization
from .scenario_helper import *
from utils import utils
from .OpenscenarioTool.osxcgenerator import XoscGenerator
from .model import Scenarios
from .scenario_helper import _validate_openscenario_configuration, DEFAULT_EVALUATION_STANDARD
from .schema import ScenariosReadDTO, AssemberScenarioCreateDTO, ScenarioTempCreateDTO, scenarios_to_tree, \
    file_child_ids_in_scenarios, delete_scenario_groups, AddScenarioGroupDir, \
    FindAllScenarios, MoveScenarioGroup, SelectIds, ScenarioIds, FindScenariosByTags, ShowScenarioGroup, \
    SearchScenarioGroup, AddScenarioGroupDirTags, OpenScenarioJson, ScenarioUpdateDTO
from utils.auth import request
from fastapi.encoders import jsonable_encoder

from ..auth.auth_casbin import AuthorityRole
from ..traffic_flow.model import TrafficFlow
from .OpenscenarioTool.oasis_xml_to_json import InnerXoscDeserializer
from pathlib import Path

router = APIRouter()


@router.put(
    "/scenarios_assemble",
    summary='创建场景',
    tags=["Scenarios"]
)
@limiter.limit("%d/minute" %TIMES)
async def create_scenario(request: Request, scenario_create_model: AssemberScenarioCreateDTO):
    user = request.state.user
    assert not await Scenarios.filter(name=scenario_create_model.name, invalid=0, company_id=user.company_id,
                                      parent_id=scenario_create_model.parent_id).first(), '场景已存在'
    scenario = Scenarios(**scenario_create_model.dict())
    scenario.user_id = user.id
    scenario.company_id = user.company_id
    await scenario.save()
    return scenario




@router.put(
    "/create_temp_scenario",
    summary='创建场景草稿',
    tags=["Scenarios"]
)
@limiter.limit("%d/minute" %TIMES)
async def create_temp_scenario(request: Request, scenario_create_model: ScenarioTempCreateDTO):
    user = request.state.user
    assert not await Scenarios.filter(name=scenario_create_model.name, invalid=0, company_id=user.company_id,
                                      parent_id=scenario_create_model.parent_id).first(), '场景已存在'
    print(scenario_create_model.dict())
    scenario = Scenarios(**scenario_create_model.dict())
    scenario.user_id = user.id
    scenario.company_id = user.company_id
    await scenario.save()
    # print('scenario:',jsonable_encoder(scenario))
    # open_scenario_json = json.dumps(scenario.open_scenario_json)
    # ui_entities_json = json.dumps(scenario.ui_entities_json)
    # scenario = jsonable_encoder(scenario)
    # scenario['open_scenario_json'] = open_scenario_json
    # scenario['ui_entities_json'] = ui_entities_json
    return scenario


@router.delete(
    "/scenarios/{scenario_id}",
    summary='删除场景',
    tags=["Scenarios"],
    dependencies=[Depends(AuthorityRole('admin'))])
@limiter.limit("%d/minute" %TIMES)
async def delete_scenario(request: Request, scenario_id: int):
    user = request.state.user
    scenario_info = await Scenarios.filter(id=scenario_id, invalid=0, company_id=user.company_id).first()
    assert scenario_info, '场景不存在'
    assert not scenario_info.system_data, '系统场景不可删除'
    scenario_info.invalid = scenario_id
    res = await scenario_info.save()
    return scenario_info


@router.put(
    "/scenarios/{scenario_id}",
    summary='更新场景',
    tags=["Scenarios"]
)
@limiter.limit("%d/minute" %TIMES)
async def update_scenario(request: Request, scenario_id: int, scenario_update_model: AssemberScenarioCreateDTO):
    user = request.state.user
    scenario_info = await Scenarios.filter(id=scenario_id, invalid=0, company_id=user.company_id).first()
    assert scenario_info, '场景不存在'
    assert not scenario_info.system_data, '系统场景不可编辑'
    if scenario_info.name != scenario_update_model.name:
        assert not await Scenarios.filter(name=scenario_update_model.name, invalid=0, parent_id=scenario_info.parent_id,
                                          company_id=user.company_id).first(), '场景名称已存在，请更换'
    scenario_dict = scenario_update_model.dict()
    scenario_dict['user_id'] = user.id
    scenario_dict['is_temp'] = 0
    scenario_dict['id'] = scenario_id

    evaluation_standard = scenario_info.evaluation_standard
    if evaluation_standard and evaluation_standard['useTemplate']:
        scenario_dict['criterion_id'] = evaluation_standard['templateId']
    res = await scenario_info.update_from_dict(scenario_dict).save()
    return scenario_dict


@router.put(
    "/update_scenarios/{scenario_id}",
    summary='更新场景',
    tags=["Scenarios"]
)
async def update_scenario(update_model: ScenarioUpdateDTO):
    user = request.state.user
    scenario_info = await Scenarios.filter(id=update_model.id, invalid=0, company_id=user.company_id).first()
    assert scenario_info, '场景不存在'

    scenario_dict = update_model.dict()
    res = await scenario_info.update_from_dict(scenario_dict).save()
    return scenario_dict


@router.put(
    "/temp_scenarios/{scenario_id}",
    summary='更新场景草稿',
    tags=["Scenarios"]
)
@limiter.limit("%d/minute" %TIMES)
async def update_temp_scenario(request: Request, scenario_id: int, scenario_update_model: ScenarioTempCreateDTO):
    user = request.state.user
    scenario_info = await Scenarios.filter(id=scenario_id, invalid=0, company_id=user.company_id).first()
    assert scenario_info, '场景不存在'
    assert not scenario_info.system_data, '系统场景不可编辑'
    if scenario_info.name != scenario_update_model.name:
        assert not await Scenarios.filter(name=scenario_update_model.name, invalid=0, parent_id=scenario_info.parent_id,
                                          company_id=user.company_id).first(), '场景名称已存在，请更换'
    scenario_dict = scenario_update_model.dict()
    scenario_dict['user_id'] = user.id
    scenario_dict['id'] = scenario_id
    scenario_dict['is_temp'] = 1
    res = await scenario_info.update_from_dict(scenario_dict).save()
    return scenario_dict


@router.post(
    "/scenarios",
    summary='查找所有场景',
    tags=["Scenarios"]
)
async def find_all_scenarios(tags_mode: FindAllScenarios):
    user = request.state.user
    scenarios_model = Scenarios.filter(Q(company_id=user.company_id) | Q(system_data=1), invalid=0)
    if tags_mode.tags:
        scenarios_model = scenarios_model.filter(tags__contains=tags_mode.tags)

    if tags_mode.content.strip() != '':
        scenarios_model = scenarios_model.filter(
            Q(name__contains=tags_mode.content) | Q(desc__contains=tags_mode.content))

    total_num = await scenarios_model.count()
    res = await scenarios_model.limit(tags_mode.pagesize).offset(
        max(0, tags_mode.pagenum - 1) * tags_mode.pagesize).all()
    pageinfo = utils.paginate(total_num, tags_mode.pagesize)
    return {'pageinfo': pageinfo, 'datas': res}


@router.get(
    "/scenarios/{scenario_id}",
    summary='查找指定id场景（get方式）',
    tags=["Scenarios"]
)
async def find_specified_scenario(scenario_id: int):
    user = request.state.user
    res = await Scenarios.filter(Q(company_id=user.company_id) | Q(system_data=1), id=scenario_id, invalid=0).first()
    assert res, '场景不存在'
    return res


@router.post(
    "/scenarios_by_ids",
    summary='查找指定id场景（post方法）',
    tags=["Scenarios"]
)
async def find_specified_scenarios(find_model: ScenarioIds):
    user = request.state.user
    # scenario_infos = await Scenarios.filter(Q(company_id=user.company_id) | Q(system_data=1), invalid=0,
    #                                         id__in=find_model.scenario_ids).all()
    scenario_infos = []
    for id in find_model.scenario_ids:
        scenario = await Scenarios.filter(Q(company_id=user.company_id) | Q(system_data=1), invalid=0, id=id).first()
        assert scenario, '存在错误的场景信息'
        scenario_infos.append(scenario)
    return scenario_infos


@router.post(
    "/scenarios_by_tags",
    summary='通过标签查找场景',
    tags=["Scenarios"]
)
async def find_scenarios_by_tags(find_model: FindScenariosByTags):
    user = request.state.user
    sql = "select {} from scenarios where (company_id = {} or system_data = 1) and invalid = 0 and JSON_OVERLAPS(tags,'{}') = 1 "
    res = await Scenarios.raw(sql.format('id', user.company_id, json.dumps(find_model.tags)))
    total_num = len(res)
    res = await Scenarios.raw(
        (sql + " limit {} offset {}").format('*', user.company_id, json.dumps(find_model.tags),
                                             find_model.pagesize,
                                             max(0, find_model.pagenum - 1) * find_model.pagesize))
    pageinfo = utils.paginate(total_num, find_model.pagesize)
    return {'pageinfo': pageinfo, 'datas': res}


@router.get(
    "/scenario_traffic_flow_blueprint",
    summary='查找指定场景',
    tags=["Scenarios"]
)
async def find_specified_scenario():
    res = await TrafficFlow.filter(invalid=0).all()
    if not res:
        init_list = []
        finename = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/blueprint.init")
        for line in open(finename):
            items = line.replace('\n', '').split(":")
            traffic_flow = TrafficFlow()
            traffic_flow.actor = items[0]
            traffic_flow.actor_class = items[1]
            init_list.append(traffic_flow)

        await TrafficFlow.bulk_create(init_list)
        res = await TrafficFlow.filter(invalid=0).all()
    return res


# ########################################### scenario-group part ##########################################
#
# ### query part
# # 返回当前user下全部场景树，生成左侧文件夹树，返回name， total， level
@router.get(
    "/scenario_group_tree",
    summary='获取场景组树',
    tags=["Scenarios"]
)
async def get_scenario_group_tree():
    user = request.state.user
    scenarios = await Scenarios.filter(Q(company_id=user.company_id) | Q(system_data=1), invalid=0).all()
    # outer_scenarios = [sce for sce in scenarios if sce.parent_id == 0 and sce.type=='file']
    trees = scenarios_to_tree(0, None, "dir", [], scenarios, 0)
    # for sce in outer_scenarios:
    #     trees["children"].append({"id": sce.id, "name": sce.name, "type": sce.type, "tags": sce.tags, "level": 1, "total": 1,
    #                     "children": '', "system_data": True})
    return trees if trees else {}


#
# # 根据文件夹parent_id返回场景信息，包括场景数量total，场景标签，第一级子场景名称，运行地图，标签，最后编辑时间, 按照先文件夹后文件顺序
@router.post(
    "/scenario_group_show",
    summary='展示场景组',
    tags=["Scenarios"]
)
async def show_scenario_group(show_model: ShowScenarioGroup):
    user = request.state.user
    sql = "select {} from scenarios where (company_id = {} or system_data = 1) and invalid = 0 and parent_id = {} "
    if show_model.tags:
        sql += "and JSON_OVERLAPS(tags,'{}') = 1".format(json.dumps(show_model.tags, ensure_ascii=False))
    if not show_model.has_temp:
        sql += " and is_temp = 0 "
    sql += " order by id desc "
    res = await Scenarios.raw(sql.format('id', user.company_id, show_model.parent_id))
    total_num = len(res)
    res = await Scenarios.raw(
        (sql + " limit {} offset {}").format('*', user.company_id, show_model.parent_id, show_model.pagesize,
                                             max(0, show_model.pagenum - 1) * show_model.pagesize))
    pageinfo = utils.paginate(total_num, show_model.pagesize)
    return {'pageinfo': pageinfo, 'datas': res}


# 在parent_id场景库下按照关键字搜索，
@router.post(
    "/scenario_group_search",
    summary='搜索场景组',
    tags=["Scenarios"]
)
async def search_scenario_group(search_model: SearchScenarioGroup):
    user = request.state.user
    sql = "select {} from scenarios where (company_id = {} or system_data = 1) and invalid = 0 and parent_id = {} "
    if search_model.tags:
        sql += " and JSON_OVERLAPS(tags,'{}') = 1".format(json.dumps(search_model.tags))

    if search_model.content:
        if search_model.content in ['`', '%', '_']:
            content = "\\" + search_model.content
        else:
            content = search_model.content
        sql += f" and (`name` like '%{content}%' or `desc` like '%{content}%' ) "
    res = await Scenarios.raw(sql.format('id', user.company_id, search_model.parent_id))
    total_num = len(res)
    res = await Scenarios.raw(
        (sql + " limit {} offset {}").format('*', user.company_id, search_model.parent_id, search_model.pagesize,
                                             max(0, search_model.pagenum - 1) * search_model.pagesize))
    pageinfo = utils.paginate(total_num, search_model.pagesize)
    return {'pageinfo': pageinfo, 'datas': res}


### command part

# 场景库新建文件夹，完成后前端场景树局部更新
@router.post(
    "/scenario_group/dir_add",
    summary='新建场景库文件夹',
    tags=["Scenarios"]
)
@limiter.limit("%d/minute" %TIMES)
async def add_scenario_group_dir(request: Request, add_model: AddScenarioGroupDir):
    user = request.state.user
    if add_model.parent_id:
        assert Scenarios.filter(type="dir", company_id=user.company_id, invalid=0,
                                id=add_model.parent_id).first(), '场景分组不存在'
    assert not await Scenarios.filter(type="dir", name=add_model.name, company_id=user.company_id, invalid=0,
                                      parent_id=add_model.parent_id).first(), '场景组名称已存在，请更换'
    scenario_model = Scenarios()
    scenario_model.name = add_model.name
    scenario_model.parent_id = add_model.parent_id
    scenario_model.type = "dir"
    if add_model.tags:
        scenario_model.tags = add_model.tags
    scenario_model.user_id = request.state.user.id
    scenario_model.company_id = user.company_id
    await scenario_model.save()
    return scenario_model


# 场景库重命名文件夹， 完成后前端场景树局部更新
@router.put(
    "/scenario_group/dir_rename",
    summary='重命名场景组文件夹',
    tags=["Scenarios"]
)
async def rename_scenario_group_dir(name: str, scenario_id: int):
    user = request.state.user
    scenario_info = await Scenarios.filter(invalid=0, company_id=user.company_id, id=scenario_id, type="dir").first()
    assert scenario_info, '场景文件夹不存在'
    assert not scenario_info.system_data, '系统场景不可更改'
    assert scenario_info.name != name, '场景名称已修改'
    assert not await Scenarios.filter(invalid=0, company_id=user.company_id, name=name, type="dir",
                                      parent_id=scenario_info.parent_id).first(), '场景组名称已存在，请更换'
    scenario_info.name = name
    res = await scenario_info.save()
    return res


# 场景库文件夹tags添加，成功后前端直接加入
@router.post(
    "/scenario_group/dir_tags_add",
    summary='添加场景组文件夹标签',
    tags=["Scenarios"]
)
async def add_scenario_group_dir_tags(add_model: AddScenarioGroupDirTags):
    user = request.state.user
    scenario_info = await Scenarios.filter(invalid=0, company_id=user.company_id, id=add_model.scenario_id).first()
    assert scenario_info, '场景不存在'
    assert not scenario_info.system_data, '系统场景不可更改'
    scenario_info.tags = add_model.tags
    res = await scenario_info.save()
    return res


# 场景库删除选中文件和文件夹， 文件夹需要递归删除，完成后前端场景树全部更新返回，同时返回右侧场景
@router.delete(
    "/scenario_group/delete",
    summary='删除场景组',
    tags=["Scenarios"],
    dependencies=[Depends(AuthorityRole('admin'))]
)
@limiter.limit("%d/minute" %TIMES)
async def delete_scenario_group(request: Request, delete_model: SelectIds):
    user = request.state.user
    scenarios = await Scenarios.filter(id__in=delete_model.select_ids, invalid=0, company_id=user.company_id,
                                       system_data=0).all()
    assert len(scenarios) == len(delete_model.select_ids), '存在错误的场景'
    for scenario in scenarios:
        await delete_scenario_groups(scenario.id, scenarios)
    new_scenarios = await Scenarios.filter(invalid=0, company_id=user.company_id).all()
    trees = scenarios_to_tree(0, None, "dir", [], new_scenarios, 0)
    return trees if trees else {}


# 场景库移动选中文件和文件夹，完成后前端场景树全部更新返回，同时返回右侧场景
@router.post(
    "/scenario-group/move",
    summary='移动场景组',
    tags=["Scenarios"]
)
async def move_scenario_group(mode_model: MoveScenarioGroup):
    user = request.state.user
    scenarios = await Scenarios.filter(id__in=mode_model.select_ids, invalid=0, company_id=user.company_id,
                                       system_data=0).all()
    assert len(scenarios) == len(mode_model.select_ids), '存在错误的场景'
    scenario_names = [scenario.name for scenario in scenarios]
    assert not await Scenarios.filter(name__in=scenario_names, invalid=0, parent_id=mode_model.parent_id,
                                      company_id=user.company_id).all(), '分组下存在相同的名称'
    await Scenarios.filter(id__in=mode_model.select_ids, invalid=0, company_id=user.company_id).update(
        parent_id=mode_model.parent_id)
    new_scenarios = await Scenarios.filter(invalid=0, company_id=user.company_id).all()
    trees = scenarios_to_tree(0, None, "dir", [], new_scenarios, 0)
    return trees if trees else {}


@router.post(
    "/open_scenario_scene",
    summary='场景格式转换',
    tags=["DynamicScenes"]
)
async def json_convert_open_scenario(open_scenario: OpenScenarioJson):
    vehicle_catalog_path = os.path.abspath(
        os.path.join("apps/scenario/OpenscenarioTool/Catalogs/Vehicles/VehicleCatalog.xosc"))
    xml_dest_path = os.path.join('/tmp/', '{}_{}.xosc'.format(str(request.state.user.id),
                                                              time.strftime("%Y%m%d-%H%M%S")))
    scenario_generation = XoscGenerator(json.dumps(open_scenario.open_scenario_json),
                                        vehicle_catalog_path, xml_dest_path)
    try:
        xosc_file_path = scenario_generation.generate_whole_file()
    except Exception:
        assert False, '场景格式转换失败'
    try:
        _validate_openscenario_configuration(xosc_file_path)
    except Exception:
        assert False, '场景格式不合规'
    with open(xosc_file_path, "r") as f:
        openscenario = f.read()
    return openscenario


@router.post(
    "/download_system_scenario",
    summary='下载系统场景',
    tags=["Scenarios"]
)
async def download_system_scenario(scenario_ids: List[int] = Body(..., embed=True)):
    user = request.state.user
    scenario_list = await Scenarios.filter(id__in=scenario_ids, invalid=0, company_id=user.company_id).all()
    assert len(scenario_list) == len(scenario_ids), '存在无效的场景'
    scenario_infos = json.dumps(jsonable_encoder(scenario_list))
    file_path = '/tmp/' + str(request.state.user.id) + 'scenario_list.json'
    f = open(file_path, 'w')
    f.write(scenario_infos)
    f.close()
    return FileResponse(file_path, filename="test.json")


@router.post(
    "/upload_system_scenario",
    summary='上传系统场景',
    tags=["Scenarios"]
)
async def upload_system_scenario(parent_id: int = Body(..., embed=True), files: UploadFile = File(...)):
    assert request.state.user.name == 'root', '非管理员不可上传'
    scenarios = json.loads(files.file.read())

    async with transactions.in_transaction() as trans:
        for s in scenarios:
            s['parent_id'] = parent_id
            s['user_id'] = 1
            s['system_data'] = 1
            sql = "replace into scenarios(name,user_id,`desc`,tags,type,parent_id,map_name,traffic_flow," \
                  "open_scenario_json,ui_entities_json,environment,evaluation_standard,is_temp,system_data) " \
                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            await trans.execute_query(sql, [s['name'], s['user_id'], s['desc'], json.dumps(s['tags']), s['type'],
                                            s['parent_id'], s['map_name'], json.dumps(s['traffic_flow']),
                                            json.dumps(s['open_scenario_json']), json.dumps(s['ui_entities_json']),
                                            json.dumps(s['environment']), json.dumps(s['evaluation_standard']),
                                            s['is_temp'], s['system_data']])

    return


@router.get(
    "/all_scenarios_by_dir_id",
    summary='根据场景id查询路径',
    tags=["Scenarios"]
)
async def find_dir_scenarios(dir_ids: str = "", sce_ids: str = ""):
    dir_id_list = dir_ids.split(",") if dir_ids else []
    sce_id_list = sce_ids.split(",") if sce_ids else []
    path_dic = {}
    prepath_list = []
    user = request.state.user
    for dir_id in dir_id_list:
        parent_path_list = []
        scenario_dir = await Scenarios.filter(id=dir_id, company_id=user.company_id, invalid=0, type='dir').first()
        if not prepath_list and scenario_dir.parent_id != 0:
            await find_dir(scenario_dir.parent_id, prepath_list)
        await get_path_dic(dir_id, path_dic, parent_path_list)
    prepath = "/".join(prepath_list[::-1])
    target_path_dic = {k: prepath + "/" + v for k, v in path_dic.items()}
    for sce_id in sce_id_list:
        scenario = await Scenarios.filter(id=sce_id, company_id=user.company_id, invalid=0).first()
        if not scenario:
            continue
        if scenario.parent_id == 0:
            target_path_dic.update({sce_id: "/" + scenario.name})
        else:
            path_list = await handel_dir_for_download(scenario.parent_id)
            target_path_dic.update({sce_id: "/".join(path_list[::-1]) + "/" + scenario.name})
    return target_path_dic


@router.post(
    "/download_scenarios",
    summary='下载场景',
    tags=["Scenarios"]
)
@limiter.limit("%d/minute" %TIMES)
async def download_scenario(request: Request, scenario_path_list: List[str] = Body(...),
                            scenario_ids: List[int] = Body(..., embed=True),
                            file_type: str = Body(...), zip_name: str = Body(...)):
    user = request.state.user
    assert len(scenario_path_list) == len(scenario_ids), "下载目录与下载数量不一致"
    scenario_list = await Scenarios.filter(id__in=scenario_ids, invalid=0, company_id=user.company_id,
                                           system_data=0).all()
    assert len(scenario_list) == len(scenario_ids), '存在无效的场景'
    assert file_type in ['cartel', 'xosc'], '不支持的下载文件类型'
    for source_dir in scenario_path_list:
        if os.path.exists(source_dir):
            shutil.rmtree(source_dir)
        os.makedirs(source_dir)
    base_path = '/tmp/'
    ret_dict = {}
    try:
        if file_type == "xosc":
            return await download_xosc(scenario_ids, user, ret_dict, scenario_path_list, zip_name, base_path)
        else:
            return await download_cartel(scenario_list, base_path, scenario_ids, user, scenario_path_list,
                                         zip_name, ret_dict)
    except:
        for dir in scenario_path_list:
            if os.path.exists(dir):
                shutil.rmtree(dir)
        ret_dict['upload_result'] = "failure"
        return ret_dict


@router.post(
    "/file_check_and_upload",
    summary='上传场景',
    tags=["Scenarios"]
)
@limiter.limit("%d/minute" %TIMES)
async def file_check_and_upload(request: Request, parent_id: int = Body(..., embed=True),
                                files: List[UploadFile] = File(...), file_type: str = Body(...),
                                for_upload: bool = Body(...), cover: bool = Body(...),
                                target_path_list: List[str] = Body(..., embed=True),
                                tags: List[str] = Body(..., embed=True)):
    assert len(target_path_list) == len(files), '目标路径与文件数量不匹配'
    assert file_type in ["xosc", "cartel"], "不支持上传的文件类型"
    user = request.state.user
    ret_dict = {}
    for idx, file in enumerate(files):
        ret_dict[file.filename] = {}
        ret_dict[file.filename]["content_error"] = []
        ret_dict[file.filename]['name_exist_error'] = ''
        ret_dict[file.filename]['upload_result'] = ''
        scenario_json, ret = upload_check(file_type, file, ret_dict)
        if not ret:
            continue
        target_path = target_path_list[idx]
        await pre_upload(target_path, file, user, ret_dict, for_upload, parent_id, scenario_json, file_type, cover)
    if tags:
        target_dir = await Scenarios.filter(name=target_path_list[0].split("/")[-1], company_id=user.company_id,
                                            invalid=0, type="dir").first()
        if target_dir:
            target_dir.tags = tags
            await target_dir.save()
    return ret_dict


@router.post(
    "/ressember_scenarios",
    summary="场景泛化",
    tags=['Scenarios']
)
@limiter.limit("%d/minute" %TIMES)
async def ressember_scenarios(request: Request, seed_id: int = Body(..., embed=True), dir_name: str = Body(..., embd=True),
                              target_path_id: int = Body(..., embed=True), scenario_num: int = Body(..., embd=True),
                              param_dict: dict = Body(..., embd=True)):
    user = request.state.user
    scenario = await Scenarios.filter(id=seed_id, invalid=0, company_id=user.company_id, system_data=0).first()
    sceanrio_name = scenario.name
    redis = request.app.state.redis
    incr_num = await redis.get(str(seed_id))
    param_dict['num'] = scenario_num
    pg = ParamGeneralization()
    json_list = pg.generalize_param(scenario.open_scenario_json, param_dict)
    scenario_name_list = []
    sce_dir = await Scenarios.filter(company_id=user.company_id, id=target_path_id, invalid=0, system_data=0).first()
    assert sce_dir, "保存路径不存在"
    parent_id = sce_dir.id
    target_dir = await Scenarios.filter(name=dir_name, user_id=user.id, invalid=0, system_data=0,
                                        parent_id=parent_id).first()

    if target_dir:
        current_scenarios = await Scenarios.filter(parent_id=target_dir.id, user_id=user.id, invalid=0,
                                                   system_data=0).all()
        current_scenarios_names = [scenario.name for scenario in current_scenarios]
    else:
        current_scenarios_names = []
    for i in range(len(json_list)):
        if not incr_num:
            await redis.incr(str(seed_id))
        while True:
            incr_num = await redis.incr(str(seed_id))
            sce_name = sceanrio_name + "_" + str(incr_num)
            if current_scenarios_names:
                if sce_name not in current_scenarios_names:
                    scenario_name_list.append(sce_name)
                    break
            else:
                scenario_name_list.append(sce_name)
                break
    return {"json_list": json_list, "scenario_name_list": scenario_name_list}