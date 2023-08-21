#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author: renpf
# datetime: 20220816
import random
import json
import copy


class ParamGeneralization(object):
    def __init__(self):
        pass

    def generalize_param(self, json_dict, param_dict, try_num=100):
        json_list = []
        for i in range(param_dict["num"]):
            one_dict = {}
            ori_json_file = copy.deepcopy(json_dict)
            light_id = self.random_light(ori_json_file, param_dict["light"])
            weather_id = self.random_weather(ori_json_file, param_dict["weather"])
            traffic_flow_num = self.random_traffic_flow(ori_json_file, param_dict["traffic_flow"])
            speed_position_param = {}
            for try_seq in range(try_num):
                speed_position_param = self.random_speed_position(ori_json_file, param_dict)
                if len(speed_position_param.keys()) > 0:
                    break
            if len(speed_position_param.keys()) == 0:
                pass
            else:
                one_dict.update({"json_dict": ori_json_file, "light_id": light_id, "weather_id": weather_id,
                                 "speed_position_param": speed_position_param, "traffic_flow_num": traffic_flow_num})
                json_list.append(one_dict)
        return json_list

    def random_light(self, ori_json_file, light_list):
        if len(light_list) > 0:
            light = random.choice(light_list)
            ori_json_file["init_environment"]["weather"]["sun_azimuth_angle"] = str(light["sun_azimuth_angle"])
            ori_json_file["init_environment"]["weather"]["sun_altitude_angle"] = str(light["sun_altitude_angle"])
            return light["id"]
        else:
            return None#not generalize light

    def random_weather(self, ori_json_file, weather_list):
        if len(weather_list) > 0:
            weather = random.choice(weather_list)
            ori_json_file["init_environment"]["weather"]["wetness"] = str(weather["wetness"])
            ori_json_file["init_environment"]["weather"]["cloudiness"] = str(weather["cloudiness"])
            ori_json_file["init_environment"]["weather"]["cloudstate"] = weather["cloudstate"]
            ori_json_file["init_environment"]["weather"]["fog_density"] = str(weather["fog_density"])
            ori_json_file["init_environment"]["weather"]["fog_falloff"] = str(weather["fog_falloff"])
            ori_json_file["init_environment"]["weather"]["fog_distance"] = str(weather["fog_distance"])
            ori_json_file["init_environment"]["weather"]["precipitation"] = str(weather["precipitation"])
            ori_json_file["init_environment"]["weather"]["sky_visibility"] = "true"
            ori_json_file["init_environment"]["weather"]["wind_intensity"] = str(weather["wind_intensity"])
            ori_json_file["init_environment"]["weather"]["fog_visualrange"] = str(weather["fog_visualrange"])
            ori_json_file["init_environment"]["weather"]["precipitation_deposits"] = str(weather["precipitation_deposits"])
            return weather["id"]
        else:
            return None

    def random_speed_position(self, ori_json_file, param_dict):
        ret_dict = {}
        if len(list(param_dict.keys())) == 0:
            return ret_dict
        for init_ent in ori_json_file["init_entities"]:
            one_dict = {}
            if param_dict[init_ent["name"]]["speed"] is not None:
                if param_dict[init_ent["name"]]["speed"]["speed_ab"] is not None: #absolute speed
                    final_sp = random.uniform(param_dict[init_ent["name"]]["speed"]["speed_ab"][0],
                                              param_dict[init_ent["name"]]["speed"]["speed_ab"][1])
                    final_sp = round(final_sp, 2)
                    init_ent["speed"]["params"]["value"] = str(final_sp)
                    one_dict.update({"speed": {"speed_ab": final_sp}})

                elif param_dict[init_ent["name"]]["speed"]["speed_diff"] is not None: # relative speed delta
                    final_sp_diff = random.uniform(param_dict[init_ent["name"]]["speed"]["speed_diff"][0],
                                                   param_dict[init_ent["name"]]["speed"]["speed_diff"][1])
                    final_sp_diff = round(final_sp_diff, 2)
                    init_ent["speed"]["params"]["value"] = str(final_sp_diff)
                    one_dict.update({"speed": {"speed_diff": final_sp_diff,
                                               "entityref": init_ent["speed"]["params"]["entityref"]}})

                elif param_dict[init_ent["name"]]["speed"]["speed_factor"] is not None: # relative speed factor
                    final_sp_factor = random.uniform(param_dict[init_ent["name"]]["speed"]["speed_factor"][0],
                                                     param_dict[init_ent["name"]]["speed"]["speed_factor"][1])
                    final_sp_factor = round(final_sp_factor, 2)
                    init_ent["speed"]["params"]["value"] = str(final_sp_factor)
                    one_dict.update({"speed": {"speed_factor": final_sp_factor,
                                               "entityref": init_ent["speed"]["params"]["entityref"]}})
                else:
                    print("no speed type")
            if param_dict[init_ent["name"]]["position"] is not None:
                if param_dict[init_ent["name"]]["position"]["position_s"] is not None: # lane position
                    final_s = random.uniform(param_dict[init_ent["name"]]["position"]["position_s"][0],
                                             param_dict[init_ent["name"]]["position"]["position_s"][1])
                    final_s = round(final_s, 2)
                    init_ent["start_position"]["params"]["s"] = str(final_s)
                    one_dict.update({"position": {"position_s": final_s}})
                elif param_dict[init_ent["name"]]["position"]["position_ds"] is not None: # relative lane position
                    final_ds = random.uniform(param_dict[init_ent["name"]]["position"]["position_ds"][0],
                                              param_dict[init_ent["name"]]["position"]["position_ds"][1])
                    final_ds = round(final_ds, 2)
                    init_ent["start_position"]["params"]["ds"] = str(final_ds)
                    one_dict.update({"position": {"position_ds": final_ds,
                                     "entityref": init_ent["start_position"]["params"]["entityref"]}})
                else:
                    print("no position type")
            ret_dict.update({init_ent["name"]: one_dict})
        if self.speed_position_fit(ret_dict, param_dict, ori_json_file):
            return ret_dict
        return {}

    def random_traffic_flow(self, ori_json_file, traffic_flow):
        if traffic_flow:
            traffic_flow_num = random.randint(traffic_flow[0], traffic_flow[1])
            ori_json_file["basic"]["traffic_flow_num"] = traffic_flow_num
            return traffic_flow_num

    def speed_position_fit(self, ret_dict, param_dict, ori_json_file):
        final_speed_dict = {}
        final_position_dict = {}
        fixed_position_list = []
        for init_ent in ori_json_file["init_entities"]:
            if param_dict[init_ent["name"]]["speed"] is None:#not generalize speed
                if init_ent["speed"]["type"] == "absolute":#absolute speed
                    final_speed_dict.update({init_ent["name"]: float(init_ent["speed"]["params"]["value"])})
            if param_dict[init_ent["name"]]["speed"] is not None:# generalize speed
                if param_dict[init_ent["name"]]["speed"]["speed_ab"] is not None: #absolute speed
                    final_speed_dict.update({init_ent["name"]: ret_dict[init_ent["name"]]["speed"]["speed_ab"]})

            if param_dict[init_ent["name"]]["position"] is None:#not generalize location
                final_position_dict.update(
                    {init_ent["name"]: {"roadid": param_dict[init_ent["name"]]["origin_info"]["roadid"],
                                        "laneid": param_dict[init_ent["name"]]["origin_info"]["laneid"],
                                        "s": float(param_dict[init_ent["name"]]["origin_info"]["s"])}})
                fixed_position_list.append(init_ent["name"])
            if param_dict[init_ent["name"]]["position"] is not None:# generalize location
                if param_dict[init_ent["name"]]["position"]["position_s"] is not None:  #lane position
                    final_position_dict.update(
                        {init_ent["name"]: {"roadid": param_dict[init_ent["name"]]["origin_info"]["roadid"],
                                            "laneid": param_dict[init_ent["name"]]["origin_info"]["laneid"],
                                            "s": float(ret_dict[init_ent["name"]]["position"]["position_s"])}})

        for seq in range(len(ori_json_file["init_entities"])):#count len(ori_json_file["init_entities"]) times
            for init_ent in ori_json_file["init_entities"]:
                if param_dict[init_ent["name"]]["speed"] is None:  #not generalize speed
                    if init_ent["speed"]["type"] == "relative":  #relative speed
                        if init_ent["speed"]["params"]["entityref"] in list(final_speed_dict.keys()):
                            if init_ent["speed"]["params"]["valuetype"] == "delta":
                                final_speed_dict.update({init_ent["name"]: float(
                                    init_ent["speed"]["params"]["value"]) + float(
                                    final_speed_dict[init_ent["speed"]["params"]["entityref"]])})
                            if init_ent["speed"]["params"]["valuetype"] == "factor":
                                final_speed_dict.update({init_ent["name"]: float(
                                    init_ent["speed"]["params"]["value"]) * float(
                                    final_speed_dict[init_ent["speed"]["params"]["entityref"]])})

                if param_dict[init_ent["name"]]["speed"] is not None:  # generalize speed
                    if init_ent["speed"]["type"] == "relative":  #relative speed
                        if init_ent["speed"]["params"]["entityref"] in list(final_speed_dict.keys()):
                            if param_dict[init_ent["name"]]["speed"]["speed_diff"] is not None:  #speed-diff
                                final_speed_dict.update({init_ent["name"]: float(
                                        ret_dict[init_ent["name"]]["speed"]["speed_diff"]) + float(
                                        final_speed_dict[init_ent["speed"]["params"]["entityref"]])})
                            if param_dict[init_ent["name"]]["speed"]["speed_factor"] is not None:  #speed-factor
                                final_speed_dict.update({init_ent["name"]: float(
                                        ret_dict[init_ent["name"]]["speed"]["speed_factor"]) * float(
                                        final_speed_dict[init_ent["speed"]["params"]["entityref"]])})

                if param_dict[init_ent["name"]]["position"] is not None:  # generalize location
                    if init_ent["start_position"]["type"] == "relativelaneposition":  # relative lane position
                        if init_ent["start_position"]["params"]["entityref"] in list(final_position_dict.keys()):
                            if param_dict[init_ent["name"]]["position"]["position_ds"] is not None:  #relative lane position
                                final_position_dict.update(
                                    {init_ent["name"]: {"roadid": param_dict[init_ent["name"]]["origin_info"]["roadid"],
                                                        "laneid": param_dict[init_ent["name"]]["origin_info"]["laneid"],
                                                        "s": float(
                                                            ret_dict[init_ent["name"]]["position"]["position_ds"]) + float(
                                                            final_position_dict[
                                                                init_ent["start_position"]["params"]["entityref"]]["s"])}})
        for k, v in final_speed_dict.items():
            if v < 0:# v<0 return false
                return False
        for k, v in final_position_dict.items():
            if v["s"] < 0 or v["s"] > param_dict[k]["origin_info"]["road_length"]:#s out of range return false
                return False
        k_list = []
        v_list = []
        for k, v in final_position_dict.items():
            k_list.append(k)
            v_list.append(v)

        for fi in range(len(v_list)):
            for se in range(len(v_list)):
                if se > fi:
                    if v_list[se]["roadid"] == v_list[fi]["roadid"] and v_list[se]["laneid"] == v_list[fi]["laneid"]:#same lane
                        if abs(v_list[se]["s"] - v_list[fi]["s"]) < 10:#distance between less than 10 return false
                            if k_list[fi] in fixed_position_list and k_list[se] in fixed_position_list:
                                continue
                            else:
                                return False
        return True

# if __name__ == "__main__":
#     json_file = r"input.json"
#     with open(json_file, "r", encoding="utf-8") as f:
#         input_dict = json.load(f)
#
#     pg = ParamGeneralization()
#     ret = pg.generalize_param(input_dict["json_dict"], input_dict["param_dict"])
#     print(ret)
