import copy
import json
import os
import shutil
import time
import zipfile
import xmlschema
from utils.auth import request
from apps.scenario.OpenscenarioTool.osxcgenerator import XoscGenerator
import xml.etree.ElementTree as ET
from starlette.responses import FileResponse
from tortoise import transactions
from .OpenscenarioTool.check_xosc import XoscChecker
from .OpenscenarioTool.oasis_xml_to_json import InnerXoscDeserializer
from .OpenscenarioTool.outer_xml_to_json import OuterXoscDeserializer
from .model import Scenarios
from pathlib import Path


async def json_convert_to_openscenario(scen_dict, car_snap, user_id):
    open_scenario_dict = scen_dict.get("open_scenario_json")
    car_model = car_snap.get("type")
    # car type add to open_scenario_json
    ego_start_postion = None
    ego_target_position = None
    for entity in open_scenario_dict.get("init_entities"):
        if "model" not in entity.keys():
            entity.update({"model": car_model})
            # get start and target position
            ego_start_postion = entity.get('start_position').get("params")
            ego_target_position = entity.get('end_position').get("params")
            break
    try:
        # convert json to xosc
        open_scenario_json_new = json.dumps(open_scenario_dict)
        vehicle_catalog_path = os.path.abspath("apps/scenario/OpenscenarioTool/Catalogs/Vehicles/VehicleCatalog.xosc")
        xml_dest_path = os.path.join('/tmp/', '{}_{}.xosc'.format(str(user_id), time.strftime("%Y%m%d-%H%M%S")))
        scenario_generation = XoscGenerator(open_scenario_json_new, vehicle_catalog_path, xml_dest_path)
        xosc_file_path = scenario_generation.generate_whole_file()
        _validate_openscenario_configuration(xosc_file_path)
        with open(xosc_file_path, "r") as f:
            openscenario = f.read()
        return openscenario, ego_start_postion, ego_target_position
    except Exception as e:
        raise e


def _validate_openscenario_configuration(openscenario_file):
    """
    Validate the given OpenSCENARIO config against the 1.0 XSD

    Note: This will throw if the config is not valid. But this is fine here.
    """
    xml_tree = ET.parse(openscenario_file)
    xsd_file = os.path.abspath("apps/scenario/OpenscenarioTool/OpenSCENARIO.xsd")
    xsd = xmlschema.XMLSchema(xsd_file)
    xsd.validate(xml_tree)

################################################################  download  ###########################################


DEFAULT_EVALUATION_STANDARD = {
    "useTemplate": False,
    "templateId": '',
    "ReachDestinationTest": True,
    "CollisionTest": True,
    "RunRedLightTest": True,
    "RoadSpeedLimitTest": True,
    "OnRoadTest": True,
    "OntoSolidLineTest": True,
    "DrivenDistanceTest": True,
    "velocity": {
        "enabled": True,
        "MinVelocityTest": 0,
        "MaxVelocityTest": 120,
    },
    "averageVelocity": {
        "enabled": True,
        "MinAverageVelocityTest": 10,
        "MaxAverageVelocityTest": 120,
    },
    "acceleration": {
        "enabled": True,
        "AccelerationLongitudinalTest": 6,
        "AccelerationLateralTest": 2.3,
        "AccelerationVerticalTest": 0.15,
    },
    "jerk": {
        "enabled": True,
        "JerkLongitudinalTest": 5,
        "JerkLateralTest": 15,
    },
}


async def download_xosc(scenario_ids, user, ret_dict, scenario_path_list, zip_name, base_path):
    xml_list = []
    source_dirs = []
    for idx, id in enumerate(scenario_ids):
        scenario = await Scenarios.filter(id=id, invalid=0, company_id=user.company_id, system_data=0).first()
        xml_path = ""
        try:
            xml_path = assember_xosc(scenario)
            _validate_openscenario_configuration(xml_path)
        except:
            ret_dict[scenario.name] = '场景转换失败或场景格式不合规'
            if xml_path:
                os.remove(xml_path)
        if not ret_dict.get(scenario.name):
            scenario_path = scenario_path_list[idx]
            source_dirs.append(scenario_path)
            try:
                dest_path = shutil.move(xml_path, scenario_path)
            except:
                os.remove(os.path.join(scenario_path, xml_path))
                dest_path = shutil.move(xml_path, scenario_path)
            xml_list.append(dest_path)
            ret_dict[scenario.name] = "success"
    if len(xml_list) == 0:
        return ret_dict
    elif len(xml_list) == 1:
        return FileResponse(xml_list[0], filename=Path(xml_list[0]).name)
    else:
        zip_name = zip_name if zip_name else "scenario"
        try:
            return zipfile_for_download(base_path, zip_name, source_dirs)
        except:
            ret_dict['upload_result'] = 'failure'


async def download_cartel(scenario_list, base_path, scenario_ids, user, scenario_path_list, zip_name, ret_dict):
    if len(scenario_list) == 1:
        file_path = '{}.cartel'.format(scenario_list[0].name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(scenario_list[0].__dict__))
        ret_dict[scenario_list[0].name] = "success"
        return FileResponse(file_path, filename=Path(file_path).name)
    else:
        for idx, id in enumerate(scenario_ids):
            scenario = await Scenarios.filter(id=id, invalid=0, company_id=user.company_id, system_data=0).first()
            scenario_path = scenario_path_list[idx]
            scenario_file_path = scenario.name + ".cartel"
            with open(scenario_file_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(scenario.__dict__))
            try:
                shutil.move(scenario_file_path, scenario_path)
            except:
                os.remove(os.path.join(scenario_path, scenario_file_path))
                shutil.move(scenario_file_path, scenario_path)
        zip_name = zip_name if zip_name else "scenario"
        try:
            return zipfile_for_download(base_path, zip_name, scenario_path_list)
        except:
            ret_dict['upload_result'] = 'failure'


async def get_path_dic(dir_id, path_dic, parent_path_list):
    user = request.state.user
    parent_dir = await Scenarios.filter(company_id=user.company_id, id=dir_id, invalid=0).first()
    parent_path_list.append(parent_dir.name)
    parent_path = "/".join(parent_path_list)
    scenarios = await Scenarios.filter(company_id=user.company_id, parent_id=dir_id, invalid=0).all()
    path_dic.update({scenario.id: parent_path + "/" +scenario.name for scenario in scenarios if scenario.type == "file"})
    dir_list = [scenario for scenario in scenarios if scenario.type == "dir"]
    if len(dir_list) == 0:
        return path_dic
    else:
        for dir in dir_list:
            path_dic.update(await get_path_dic(dir.id, path_dic, parent_path_list))
        return path_dic


async def find_dir(parent_id, path_list):
    user = request.state.user
    scenario_dir = await Scenarios.filter(id=parent_id, company_id=user.company_id, invalid=0, type='dir').first()
    path_list.append(scenario_dir.name)
    if scenario_dir.parent_id == 0:
        return path_list
    else:
        await find_dir(scenario_dir.parent_id, path_list)


async def handel_dir_for_download(parent_id):
    user = request.state.user
    path_list = []
    current_dir = await Scenarios.filter(id=parent_id, invalid=0, company_id=user.company_id, system_data=0).first()
    assert current_dir, 'oasis内部文件不支持此操作'
    parent_dir_id = current_dir.parent_id
    if parent_dir_id == 0:
        path_list.append(current_dir.name)
    else:
        path_list.append(current_dir.name)
        await find_dir(parent_dir_id, path_list)
    return path_list


def zipfile_for_download(base_path, zip_name, source_dir_list):
    if "." in zip_name:
        zip_name = zip_name.split(".")[0]
    zip_path = os.path.join(base_path, '{}_{}.zip'.format(zip_name, time.strftime("%H%M%S")))
    with zipfile.ZipFile(zip_path, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        target_dir_list = source_dir_list
        for ori_source_dir in source_dir_list:
            if "/" in ori_source_dir:
                idx_list = [idx for idx, str in enumerate(ori_source_dir) if str == "/"]
                target_dir_list.extend([ori_source_dir[:idx] for idx in idx_list])
        target_dir_list = list(set(target_dir_list))
        target_dir_list.sort()
        for source_dir in target_dir_list:
            pre_len = len(os.path.dirname(source_dir))
            for parent, dirnames, filenames in os.walk(source_dir):
                for filename in filenames:
                    pathfile = os.path.join(parent, filename)
                    arcname = pathfile[pre_len:].strip(os.path.sep)
                    zf.write(pathfile, arcname)
                    os.remove(pathfile)
    return FileResponse(zip_path, filename=Path(zip_path).name)


########################################################## upload ####################################################


def assember_xosc(scenario):
    vehicle_catalog_path = os.path.abspath(
        os.path.join("apps/scenario/OpenscenarioTool/Catalogs/Vehicles/VehicleCatalog.xosc"))
    xml_dest_path = '{}.xosc'.format(scenario.name)
    scenario_generation = XoscGenerator(json.dumps(scenario.open_scenario_json),
                                        vehicle_catalog_path, xml_dest_path)
    xml_file_path = scenario_generation.generate_whole_file()
    return xml_file_path


def upload_check(file_type, file, ret_dict):
    if file_type == "xosc":
        try:
            file_obj = copy.deepcopy(file)
            _validate_openscenario_configuration(file_obj.file)
        except:
            ret_dict[file.filename]["content_error"].append('场景格式不合规')
        try:
            tree = ET.parse(file.file)
            root = tree.getroot()
            author = root.find("FileHeader").attrib.get('author')
            xosc_checker = XoscChecker()
            ret = xosc_checker.check(root, ret_dict[file.filename]["content_error"])
            if author in ['oasis', 'guardstrike']:
                json_deser = InnerXoscDeserializer(file.file)
                scenario_json = json_deser.deserialize(root)
            else:
                json_deser = OuterXoscDeserializer(file.file)
                scenario_json = json_deser.deserialize(root)
            return scenario_json, ret
        except:
            ret_dict[file.filename]["content_error"].append('xosc反序列化校验失败')
            return "", False
    else:
        try:
            scenario_json = file.file.read().decode('utf-8')
            vehicle_catalog_path = os.path.abspath(
                os.path.join("apps/scenario/OpenscenarioTool/Catalogs/Vehicles/VehicleCatalog.xosc"))
            xml_dest_path = '{}.xosc'.format(file.filename)
            scenario_dic = json.loads(scenario_json)
            scenario_generation = XoscGenerator(json.dumps(scenario_dic.get('open_scenario_json')),
                                                vehicle_catalog_path, xml_dest_path)
            xml_file_path = scenario_generation.generate_whole_file()
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            xosc_checker = XoscChecker()
            ret = xosc_checker.check(root, ret_dict[file.filename]["content_error"])
            return scenario_json, ret
        except:
            ret_dict[file.filename]["content_error"].append('Cartel解析校验失败')
            return "", False


async def pre_upload(target_path, file, user, ret_dict, for_upload, parent_id, scenario_json, file_type, cover):
    scenario_name = file.filename.split(".")[0]
    dir_name_list = []
    if not target_path:
        current_scenarios = await Scenarios.filter(name=file.filename.split('.')[0], invalid=0, parent_id=parent_id,
                                                   company_id=user.company_id).all()
        current_scenarios_names = [scenario.name for scenario in current_scenarios]
        if scenario_name in current_scenarios_names:
            ret_dict[file.filename]['name_exist_error'] = '场景库已有同名场景'
        if for_upload and (not ret_dict[file.filename]['name_exist_error'] or cover) and not \
                ret_dict[file.filename]['content_error']:
            info = await upload_scenario(parent_id, scenario_json, file_type, cover, scenario_name,
                                         ret_dict[file.filename], dir_name_list, user)
            ret_dict[file.filename]['upload_result'] = info
        elif for_upload and not ret_dict[file.filename]['name_exist_error'] and not cover:
            ret_dict[file.filename]['upload_result'] = 'failure'
    else:
        dir_name_list = target_path.split("/")
        async with transactions.in_transaction():
            parent_dir_id = parent_id
            for dir_path in dir_name_list:
                current_dir = await Scenarios.filter(name=dir_path, parent_id=parent_dir_id, invalid=0,
                                                     company_id=user.company_id, type="dir").first()
                if current_dir:
                    parent_dir_id = current_dir.id
                    continue
            if parent_dir_id != parent_id:
                current_scenarios = await Scenarios.filter(name=file.filename.split(".")[0], invalid=0,
                                                           parent_id=parent_dir_id, company_id=user.company_id).all()
                current_scenarios_names = [scenario.name for scenario in current_scenarios]
                if scenario_name in current_scenarios_names:
                    ret_dict[file.filename]['name_exist_error'] = '场景库已有同名场景'
            if for_upload and (not ret_dict[file.filename]['name_exist_error'] or cover) and \
                    not ret_dict[file.filename]['content_error']:
                info = await upload_scenario(parent_id, scenario_json, file_type, cover, scenario_name,
                                             ret_dict[file.filename], dir_name_list, user)
                ret_dict[file.filename]['upload_result'] = info
            elif for_upload and not ret_dict[file.filename]['name_exist_error'] and not cover:
                ret_dict[file.filename]['upload_result'] = 'failure'


async def upload_scenario(parent_id, scenario_json, file_type, cover, scenario_name, ret_dict, dir_name_list, user):
    parent_dir_id = parent_id
    for dir_path in dir_name_list:
        current_dir = await Scenarios.filter(name=dir_path, parent_id=parent_dir_id, invalid=0,
                                             company_id=user.company_id, type="dir").first()
        if current_dir:
            parent_dir_id = current_dir.id
            continue
        scenario_dir = Scenarios()
        scenario_dir.name = dir_path
        scenario_dir.parent_id = parent_dir_id
        scenario_dir.type = "dir"
        scenario_dir.user_id = user.id
        scenario_dir.company_id = user.company_id
        await scenario_dir.save()
        parent_dir_id = scenario_dir.id

    scenario_dic = json.loads(scenario_json)
    scenario_dic['name'] = scenario_name
    scenario_param = dict()
    if file_type == 'xosc':
        weather_dict = scenario_dic["init_environment"]['weather']
        weather_params = {}
        try:
            scenario_param = assermber_xosc(scenario_param, weather_dict, weather_params, scenario_dic, parent_dir_id)
            if cover and ret_dict['name_exist_error']:
                return await cover_xosc_scenario(scenario_param, user, parent_id)
            else:
                scenario = Scenarios(**scenario_param)
                await scenario.save()
        except:
            return "failure"
    else:
        if cover and ret_dict['name_exist_error']:
            return await cover_cartel_scenario(scenario_dic, user, parent_dir_id)
        else:
            scenario_dic['parent_id'] = parent_dir_id
            scenario_dic['user_id'] = user.id
            scenario_dic['company_id'] = user.company_id
            scenario_dic.pop('id', '')
            scenario_dic.pop('system_data', '')
            scenario_dic.pop('tags', '')
            scenario = Scenarios(**scenario_dic)
            await scenario.save()
    return 'success'


def assermber_xosc(scenario_param, weather_dict, weather_params, scenario_dic, parent_id):
    for k, v in weather_dict.items():
        if k == "sky_visibility" and v == "true":
            weather_params[k] = True
        elif k == "sky_visibility" and v == "false":
            weather_params[k] = False
        elif k == "cloudstate":
            weather_params[k] = v
        else:
            weather_params[k] = float(v)
    weather_params.pop('sun_azimuth_angle', None)
    weather_params.pop('sun_altitude_angle', None)
    environment = {'light_param': {'sun_azimuth_angle': float(weather_dict['sun_azimuth_angle']),
                                   'sun_altitude_angle': float(weather_dict['sun_altitude_angle'])},
                   'weather_param': weather_params}
    scenario_param['parent_id'] = parent_id
    scenario_param['user_id'] = request.state.user.id
    scenario_param['company_id'] = request.state.user.company_id
    scenario_param['name'] = scenario_dic['name']
    scenario_param['map_name'] = scenario_dic['basic']['xodr']
    scenario_param['open_scenario_json'] = json.dumps(scenario_dic)
    scenario_param['environment'] = environment
    scenario_param['traffic_flow'] = []
    scenario_param['type'] = 'file'
    scenario_param["evaluation_standard"] = DEFAULT_EVALUATION_STANDARD
    return scenario_param


async def cover_xosc_scenario(scenario_param, user, parent_id):
    try:
        scenarioname = scenario_param['name']
        scenario = await Scenarios.filter(name=scenarioname, company_id=user.company_id, invalid=0, parent_id=parent_id).first()
        scenario.name = scenarioname
        scenario.map_name = scenario_param['map_name']
        scenario.open_scenario_json = scenario_param['open_scenario_json']
        scenario.ui_entities_json = None
        scenario.environment = scenario_param['environment']
        scenario.evaluation_standard = scenario_param['evaluation_standard']
        scenario.type = scenario_param['type']
        scenario.company_id = user.company_id
        scenario.traffic_flow = scenario_param['traffic_flow']
        scenario.user_id = user.id
        await scenario.save()
        return 'success'
    except:
        return 'failure'


async def cover_cartel_scenario(scenario_dic, user, parent_id):
    try:
        scenarioname = scenario_dic['name']
        scenario = await Scenarios.filter(name=scenarioname, company_id=user.company_id, invalid=0, parent_id=parent_id).first()
        scenario_dic.pop('id', '')
        scenario_dic['ui_entities_json'] = None
        scenario_dic['name'] = scenarioname
        scenario_dic['parent_id'] = parent_id
        scenario_dic['user_id'] = user.id
        scenario_dic['company_id'] = user.company_id
        await scenario.update_from_dict(scenario_dic).save()
        return 'success'
    except:
        return 'failure'