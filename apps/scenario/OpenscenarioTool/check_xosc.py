#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author: renpf
# datetime: 20221129

import json
import math
import logging
import xml.etree.ElementTree as ET


class TriggerCollector(object):
    """
    class for convert xosc event starttrigger to json.
    """
    def __init__(self):
        pass

    def collect_by_entity_condition(self, obj):
        """
        @param obj: elementtree node of ByEntityCondition
        @type obj: elementtree
        @param edge: condition edge
        @type edge: str
        @param delay: condition delay
        @type delay: str
        @return: a dict structure of given ByEntityCondition
        @rtype: dict
        """
        ret = []

        for obj_1 in obj.find("EntityCondition"):
            ret.append(obj_1.tag)

        return ret

    def collect_by_value_condition(self, obj):
        """
        @param obj: elementtree node of ByValueCondition
        @type obj: elementtree
        @param edge: condition edge
        @type edge: str
        @param delay: condition delay
        @type delay: str
        @return: a dict structure of given ByValueCondition
        @rtype: dict
        """
        ret = []

        for obj_1 in obj:
            ret.append(obj_1.tag)

        return ret

    def collect(self, obj):
        """
        @param obj: elementtree node of Event
        @type obj: elementtree
        @return: a list structure of given Event StartTrigger
        @rtype: list
        """
        ret = []
        for obj_1 in obj.find("StartTrigger"):
            if obj_1.tag == "ConditionGroup":#ConditionGroup level
                for obj_2 in obj_1:
                    if obj_2.tag == "Condition":#Condition level
                        if obj_2.find("ByEntityCondition") != None:
                            ret.extend(self.collect_by_entity_condition(obj_2.find("ByEntityCondition")))
                        if obj_2.find("ByValueCondition") != None:
                            ret.extend(self.collect_by_value_condition(obj_2.find("ByValueCondition")))
        return ret


class ActionCollector(object):
    """
    class for convert xosc event action to json.
    """
    def __init__(self):
        pass

    def collect(self, obj):
        """
        @param obj: elementtree node of Event
        @type obj: elementtree
        @return: a list structure of given Event Action
        @rtype: list
        """
        ret = []
        for obj_1 in obj:
            if obj_1.tag == "Action":
                if obj_1.find("PrivateAction") is not None:
                    for obj_2 in obj_1.find("PrivateAction"):
                        if obj_2.tag == "LongitudinalAction":
                            if obj_2.find("SpeedAction") != None:
                                ret.append("SpeedAction")
                            if obj_2.find("LongitudinalDistanceAction") != None:
                                ret.append("LongitudinalDistanceAction")

                        if obj_2.tag == "LateralAction":
                            if obj_2.find("LaneChangeAction") != None:
                                ret.append("LaneChangeAction")
                            if obj_2.find("LaneOffsetAction") != None:
                                ret.append("LaneOffsetAction")
                            if obj_2.find("LateralDistanceAction") != None:
                                ret.append("LateralDistanceAction")

                        if obj_2.tag == "SynchronizeAction":
                            ret.append("SynchronizeAction")

                        if obj_2.tag == "RoutingAction":
                            if obj_2.find("AssignRouteAction") != None:
                                ret.append("AssignRouteAction")
                            if obj_2.find("FollowTrajectoryAction") != None:
                                ret.append("FollowTrajectoryAction")
                            if obj_2.find("AcquirePositionAction") != None:
                                ret.append("AcquirePositionAction")

                        if obj_2.tag == "TeleportAction":
                            ret.append("TeleportAction")

                if obj_1.find("GlobalAction") is not None:
                    for obj_2 in obj_1.find("GlobalAction"):
                        if obj_2.tag == "InfrastructureAction":
                            if obj_2.find("TrafficSignalAction") != None:
                                if obj_2.find("TrafficSignalAction").find("TrafficSignalStateAction") != None:
                                    ret.append("TrafficSignalStateAction")
        return ret


class XoscChecker(object):

    def __init__(self):
        """

        """
        default_map_list = [
            {
                "img": 'town_1',
                "map_name": 'Town01',
                id: 1,
                "desc": '一个基本的城镇布局，包括所有的“T型路口”。',
            },
            {
                "img": 'town_2',
                "map_name": 'Town02',
                id: 2,
                "desc": '与Town01相似，但更小。',
            },
            {
                "img": 'town_3',
                "map_name": 'Town03',
                id: 3,
                "desc": '最复杂的城镇，有5车道交叉口、环形交叉口、不平路面、隧道等等，是一种混合地图。',
            },
            {
                "img": 'town_4',
                "map_name": 'Town04',
                id: 4,
                "desc": '一个包括了高速公路和环岛的小镇。',
            },
            {
                "img": 'town_5',
                "map_name": 'Town05',
                id: 5,
                "desc": '方形网格城镇，有交叉路口和一座桥。每个方向都有多条车道，可用于测试变道场景。',
            },
            {
                "img": 'Crossroad',
                "map_name": 'Crossroad',
                id: 30,
                "desc": '十字路口，双向二车道，无红路灯',
            },
            {
                "img": 'Curve',
                "map_name": 'Curve',
                id: 31,
                "desc": '弯道，双向四车道，长度1155米',
            },
            {
                "img": 'highway2-6-1000',
                "map_name": 'highway2-6-1000',
                id: 32,
                "desc": '高速直道，双向六车道，含有两个单车道匝道和一个二车道匝道',
            },
            {
                "img": 'Park',
                "map_name": 'Park',
                id: 33,
                "desc": '停车场',
            },
            {
                "img": 'Long-Straight',
                "map_name": 'Long-Straight',
                id: 36,
                "desc": '长直道，双向六车道，长度3000米',
            },
            {
                "img": 'T-junction',
                "map_name": 'T-junction',
                id: 35,
                "desc": '丁字路口，双向二车道，无红路灯',
            }
        ]
        self.map_list = [ele["map_name"] for ele in default_map_list]
        # print(self.map_list)
        self.init_entity_list = []
        self.paramerter_declaration_dict = {}
        self.position_list = ["WorldPosition", "RelativeWorldPosition", "RelativeObjectPosition", "RoadPosition",
                              "RelativeRoadPosition", "LanePosition", "RelativeLanePosition"]
        self.support_action_list = ["SpeedAction", "LongitudinalDistanceAction", "LaneChangeAction", "LaneOffsetAction",
                                    "LateralDistanceAction", "SynchronizeAction", "AssignRouteAction",
                                    "FollowTrajectoryAction", "AcquirePositionAction", "TeleportAction",
                                    "TrafficSignalStateAction"]
        self.support_trigger_list = ["CollisionCondition", "OffroadCondition", "TimeHeadwayCondition",
                                     "TimeToCollisionCondition", "AccelerationCondition", "StandStillCondition",
                                     "SpeedCondition", "RelativeSpeedCondition", "TraveledDistanceCondition",
                                     "ReachPositionCondition", "DistanceCondition", "RelativeDistanceCondition",
                                     "TimeOfDayCondition", "SimulationTimeCondition", "TrafficSignalCondition"]

    def get_ParameterDeclaration(self, obj):
        if not obj.find("ParameterDeclarations"):
            return
        for obj_1 in obj.find("ParameterDeclarations"):
            self.paramerter_declaration_dict.update({obj_1.attrib["name"]: obj_1.attrib["value"]})
        if obj.find("Storyboard").find("Init").find("ParameterDeclarations") is not None:
            for obj_1 in obj.find("Storyboard").find("Init").find("ParameterDeclarations"):
                self.paramerter_declaration_dict.update({obj_1.attrib["name"]: obj_1.attrib["value"]})
        if obj.find("Storyboard").find("Story").find("ParameterDeclarations") is not None:
            for obj_1 in obj.find("Storyboard").find("Story").find("ParameterDeclarations"):
                self.paramerter_declaration_dict.update({obj_1.attrib["name"]: obj_1.attrib["value"]})

    def get_real_parameter(self, input_parameter):
        """
        change parameter declaration to real value
        @param input_parameter: real value or parameter declaration
        @type input_parameter: str
        @return: real value
        @rtype: str
        """
        if input_parameter in list(self.paramerter_declaration_dict.keys()):
            return self.paramerter_declaration_dict[input_parameter] if "ego" not in self.paramerter_declaration_dict[
                input_parameter].lower() else "ego_vehicle"
        else:
            return input_parameter if "ego" not in input_parameter.lower() else "ego_vehicle"

    def deserialize_Entities(self, obj):
        """
        @param obj: elementtree node of Entity
        @type obj: elementtree
        @return: update self.json_dict
        @rtype:
        """
        for obj_1 in obj:
            if obj_1.tag == "ScenarioObject":
                name = self.get_real_parameter(obj_1.attrib["name"])
                if name == "ego_vehicle":
                    self.init_entity_list.append({"name": name, "type": "vehicle"})
                    continue

                for obj_2 in obj_1:
                    if obj_2.tag == "Vehicle":
                        v = obj_2.attrib["vehicleCategory"]
                        if v == "car":
                            self.init_entity_list.append({"name": name, "type": "vehicle"})
                        if v == "van":
                            self.init_entity_list.append({"name": name, "type": "vehicle"})
                        if v == "truck":
                            self.init_entity_list.append({"name": name, "type": "vehicle"})
                        if v == "motorbike":
                            self.init_entity_list.append({"name": name, "type": "vehicle"})
                        if v == "bicycle":
                            self.init_entity_list.append({"name": name, "type": "vehicle"})

                    if obj_2.tag == "Pedestrian":
                        self.init_entity_list.append({"name": name, "type": "pedestrian"})


    def check_openscenario_parameters(self, obj, actor, ret_list):
        """
        :param obj: Node of ManeuverGroup
        :type obj: ElementTree Node
        :return:
        :rtype:
        """
        for ent in self.init_entity_list:
            if ent["name"] == actor:
                actor_type = ent["type"]
        if actor_type == "pedestrian":
            #pedestrain-lateraldistanceaction and pedestrain-longitudinaldistanceaction
            #and pedestrain-laneoffsetaction not support
            if obj.find("Maneuver") is not None:
                for obj_1 in obj.find("Maneuver"):
                    if obj_1.tag == "Event":
                        if obj_1.find("Action").find("PrivateAction") is not None:
                            if obj_1.find("Action").find("PrivateAction").find("LongitudinalAction") is not None:
                                if obj_1.find("Action").find("PrivateAction").find("LongitudinalAction").find(
                                    "LongitudinalDistanceAction") is not None:
                                    ret_list.append("行人{}不能执行纵向距离保持动作".format(actor))
                                    return False
                            if obj_1.find("Action").find("PrivateAction").find("LateralAction") is not None:
                                if obj_1.find("Action").find("PrivateAction").find("LateralAction").find(
                                    "LateralDistanceAction") is not None:
                                    ret_list.append("行人{}不能执行横向距离保持动作".format(actor))
                                    return False
                                if obj_1.find("Action").find("PrivateAction").find("LateralAction").find(
                                    "LaneOffsetAction") is not None:
                                    ret_list.append("行人{}不能执行车道偏移动作".format(actor))
                                    return False
        else:
            # pedestrain-lateraldistanceaction and pedestrain-longitudinaldistanceaction not support
            pass
        return True

    def check_ego_exists(self, obj, ret_list):
        entity_list = []
        for obj_1 in obj:
            if obj_1.tag == "ScenarioObject":
                name = self.get_real_parameter(obj_1.attrib["name"])
                entity_list.append(name)
        ego_num = 0
        for ent in entity_list:
            if "ego" in ent.lower():
                ego_num += 1
        if ego_num == 0:
            ret_list.append("主车缺失")
            return False
        elif ego_num > 1:
            ret_list.append("不支持多个主车")
            return False
        else:
            return True

    def check_map_exists(self, obj, ret_list):
        xodr = ""
        for obj_1 in obj:
            if obj_1.tag == "LogicFile":
                xodr = self.get_real_parameter(obj_1.attrib["filepath"])
                break
        if xodr in self.map_list:
            return True
        else:
            ret_list.append("地图{}不存在".format(xodr))

    def check_unsupported_trigger_action(self, obj, ret_list):
        action_list = []
        trigger_list = []
        for obj_1 in obj:
            if obj_1.tag == "ManeuverGroup" and obj_1.find("Maneuver") is not None:
                if obj_1.find("Actors") is not None:
                    if obj_1.find("Actors").find("EntityRef") is not None:
                        actor = self.get_real_parameter(obj_1.find("Actors").find("EntityRef").attrib["entityRef"])
                        if actor == "ego_vehicle":
                            continue
                        else:
                            self.check_openscenario_parameters(obj_1, actor, ret_list)
                    else:
                        ret_list.append("{}没有动作执行者".format(obj_1.attrib["name"]))
                        return False
                for obj_2 in obj_1.find("Maneuver"):
                    if obj_2.tag == "Event":
                        trigger_generator = TriggerCollector()
                        action_generator = ActionCollector()
                        trigger_one_ret = trigger_generator.collect(obj_2)
                        action_one_ret = action_generator.collect(obj_2)
                        trigger_list.extend(trigger_one_ret)
                        action_list.extend(action_one_ret)

        for act in action_list:
            if act not in self.support_action_list:
                ret_list.append("不支持{}动作".format(act))
                return False
        for tri in trigger_list:
            if tri not in self.support_trigger_list:
                ret_list.append("不支持{}条件".format(tri))
                return False
        return True

    def check_all_init_position(self, obj, ret_list):
        for obj_1 in obj:
            if obj_1.tag == "Private":# and "ego" in obj_1.attrib["entityRef"].lower():
                if_has_init_position = False
                for obj_2 in obj_1:
                    if obj_2.find("TeleportAction") is not None:
                        if obj_2.find("TeleportAction").find("Position") is not None:
                            if obj_2.find("TeleportAction").find("Position")[0].tag in self.position_list:
                                if_has_init_position = True
                                break
                if not if_has_init_position:
                    ret_list.append("{}初始位置缺失".format(obj_1.attrib["entityRef"]))
                    return False
        return True

    def check_all_init_speed(self, obj, ret_list):
        for obj_1 in obj:
            if obj_1.tag == "Private":# and "ego" in obj_1.attrib["entityRef"].lower():
                if_has_init_speed = False
                for obj_2 in obj_1:
                    if obj_2.find("LongitudinalAction") is not None:
                        if obj_2.find("LongitudinalAction").find("SpeedAction") is not None:
                            if obj_2.find("LongitudinalAction").find("SpeedAction").find("SpeedActionTarget") is not None:
                                if_has_init_speed = True
                                break
                if not if_has_init_speed:
                    ret_list.append("{}初始速度缺失".format(obj_1.attrib["entityRef"]))
                    return False
        return True

    def check_catalog_exists(self, obj, ret_list):
        for obj_1 in obj:

            if obj_1 is not None:
                ret_list.append("使用了不支持的CatalogLocations")
                return False
            else:
                return True
        return True

    def check(self, root, ret_list):
        try:
            self.get_ParameterDeclaration(root)
            self.deserialize_Entities(root.find("Entities"))
            c1 = self.check_catalog_exists(root.find("CatalogLocations"), ret_list)
            if not c1:
                return False
            c2 = self.check_ego_exists(root.find("Entities"), ret_list)
            if not c2:
                return False
            c3 = self.check_map_exists(root.find("RoadNetwork"), ret_list)
            if not c3:
                return False
            c4 = self.check_unsupported_trigger_action(root.find("Storyboard").find("Story").find("Act"), ret_list)
            if not c4:
                return False
            c5 = self.check_all_init_position(root.find("Storyboard").find("Init").find("Actions"), ret_list)
            if not c5:
                return False
            c6 = self.check_all_init_speed(root.find("Storyboard").find("Init").find("Actions"), ret_list)
            if not c6:
                return False
            return True
        except Exception as e:
            # print(e)
            ret_list.append("xosc 校验失败")
            return False


# if __name__ == "__main__":
#     # filename1 = "./xosc/SynchronizedArrivalToIntersection.xosc"
#     # filename1 = "./xosc/TrafficJam.xosc"
#     # filename1 = "./xosc/EndofTrafficJamNeighboringLaneOccupied.xosc"
#     # filename1 = "./xosc/FastOvertakeWithReInitialization.xosc"
#     # filename1 = "./xosc/CutIn.xosc"
#     # filename1 = "./xosc/DoubleLaneChanger.xosc"
#     # filename1 = "./xosc/EndOfTrafficJam.xosc"
#     # filename1 = "./xosc/Overtaker.xosc"
#     # filename1 = "./xosc/SlowPrecedingVehicle.xosc"
#     # filename1 = "./xosc/rpf1-uploadchange.xosc"
#     filename1 = r"E:\project\auto_drive_test\scenario\trafficsignal\test\ts-action-test-oasis.xosc"
#     ixd = XoscChecker()
#     tree = ET.parse(filename1)
#     root = tree.getroot()
#     ret_list = []
#     ret = ixd.check(root, ret_list)
#     print(ret_list)
