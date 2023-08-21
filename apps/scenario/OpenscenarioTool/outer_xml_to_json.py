#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author: renpf
# datetime: 20221128

import xml.etree.ElementTree as ET
import json
import math
import logging
logging.basicConfig(filename='./log.txt', level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s')

paramerter_declaration_dict = {}

def get_real_parameter(input_parameter):
    """
    change parameter declaration to real value
    @param input_parameter: real value or parameter declaration
    @type input_parameter: str
    @return: real value
    @rtype: str
    """
    if input_parameter in list(paramerter_declaration_dict.keys()):
        return paramerter_declaration_dict[input_parameter] if "ego" not in paramerter_declaration_dict[
            input_parameter].lower() else "ego_vehicle"
    else:
        return input_parameter if "ego" not in input_parameter.lower() else "ego_vehicle"

class PositionGenerator(object):
    """
    class for convert xosc positon to json.
    """
    def __init__(self):
        pass

    def convert_angle_to_rad(self, angle):
        """
        @param angle: position hpr angle
        @type angle: str
        @return: position hpr rad
        @rtype: str
        """
        return str(float(angle) / 180 * math.pi)

    def convert_rad_to_angle(self, rad):
        """
        @param angle: position hpr rad
        @type angle: str
        @return: position hpr angle
        @rtype: str
        """
        if "e" in rad:
            rad = rad[:rad.index("e")]
        return str(float(rad) / math.pi * 180)

    def get_Orientation(self, obj_1):
        orientation = {}
        if obj_1.find("Orientation") is not None:
            reftype = get_real_parameter(obj_1.find("Orientation").attrib["reftype"]) if "reftype" in list(
                obj_1.attrib.keys()) else "absolute"
            orientation.update({"reftype": reftype})
            h = self.convert_rad_to_angle(
                get_real_parameter(obj_1.find("Orientation").attrib["h"])) if "h" in list(
                obj_1.find("Orientation").attrib.keys()) else "0.0"
            orientation.update({"h": h})
            p = self.convert_rad_to_angle(
                get_real_parameter(obj_1.find("Orientation").attrib["p"])) if "p" in list(
                obj_1.find("Orientation").attrib.keys()) else "0.0"
            orientation.update({"p": p})
            r = self.convert_rad_to_angle(
                get_real_parameter(obj_1.find("Orientation").attrib["r"])) if "r" in list(
                obj_1.find("Orientation").attrib.keys()) else "0.0"
            orientation.update({"r": r})
        else:
            reftype = "absolute"
            orientation.update({"reftype": reftype})
            h = "0.0"
            orientation.update({"h": h})
            p = "0.0"
            orientation.update({"p": p})
            r = "0.0"
            orientation.update({"r": r})
        return orientation

    def generate(self, obj):
        """
        @param obj: elementtree node of Position
        @type obj: elementtree
        @return: a dict structure of given Position
        @rtype: dict
        """
        ret = {}
        try:
            for obj_1 in obj:
                if obj_1.tag == "WorldPosition":
                    ret["type"] = "worldposition"
                    ret["params"] = {}
                    x = get_real_parameter(obj_1.attrib["x"]) if "x" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"x": x})
                    y = get_real_parameter(obj_1.attrib["y"]) if "y" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"y": y})
                    z = get_real_parameter(obj_1.attrib["z"]) if "z" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"z": z})
                    h = self.convert_rad_to_angle(get_real_parameter(obj_1.attrib["h"])) if "h" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"h": h})
                    p = self.convert_rad_to_angle(get_real_parameter(obj_1.attrib["p"])) if "p" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"p": p})
                    r = self.convert_rad_to_angle(get_real_parameter(obj_1.attrib["r"])) if "r" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"r": r})

                elif obj_1.tag == "RelativeWorldPosition":
                    ret["type"] = "relativeworldposition"
                    ret["params"] = {}
                    entityref = get_real_parameter(obj_1.attrib["entityRef"])
                    ret["params"].update({"entityref": entityref})
                    dx = get_real_parameter(obj_1.attrib["dx"]) if "dx" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"dx": dx})
                    dy = get_real_parameter(obj_1.attrib["dy"]) if "dy" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"dy": dy})
                    dz = get_real_parameter(obj_1.attrib["dz"]) if "dz" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"dz": dz})
                    orientation = self.get_Orientation(obj_1)
                    ret["params"].update({"orientation": orientation})

                elif obj_1.tag == "RelativeObjectPosition":
                    ret["type"] = "relativeobjectposition"
                    ret["params"] = {}
                    entityref = get_real_parameter(obj_1.attrib["entityRef"])
                    ret["params"].update({"entityref": entityref})
                    dx = get_real_parameter(obj_1.attrib["dx"]) if "dx" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"dx": dx})
                    dy = get_real_parameter(obj_1.attrib["dy"]) if "dy" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"dy": dy})
                    dz = get_real_parameter(obj_1.attrib["dz"]) if "dz" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"dz": dz})
                    orientation = self.get_Orientation(obj_1)
                    ret["params"].update({"orientation": orientation})

                elif obj_1.tag == "LanePosition":
                    ret["type"] = "laneposition"
                    ret["params"] = {}
                    roadid = get_real_parameter(obj_1.attrib["roadId"]) if "roadId" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"roadid": roadid})
                    laneid = get_real_parameter(obj_1.attrib["laneId"]) if "laneId" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"laneid": laneid})
                    offset = get_real_parameter(obj_1.attrib["offset"]) if "offset" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"offset": offset})
                    s = get_real_parameter(obj_1.attrib["s"]) if "s" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"s": s})
                    orientation = self.get_Orientation(obj_1)
                    ret["params"].update({"orientation": orientation})

                elif obj_1.tag == "RelativeLanePosition":
                    ret["type"] = "relativelaneposition"
                    ret["params"] = {}
                    entityref = get_real_parameter(obj_1.attrib["entityRef"])
                    ret["params"].update({"entityref": entityref})
                    offset = get_real_parameter(obj_1.attrib["offset"]) if "offset" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"offset": offset})
                    ds = get_real_parameter(obj_1.attrib["ds"]) if "ds" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"ds": ds})
                    dlane = get_real_parameter(obj_1.attrib["dLane"]) if "dLane" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"dlane": dlane})
                    orientation = self.get_Orientation(obj_1)
                    ret["params"].update({"orientation": orientation})

                elif obj_1.tag == "RoadPosition":
                    ret["type"] = "roadposition"
                    ret["params"] = {}
                    roadid = get_real_parameter(obj_1.attrib["roadId"]) if "roadId" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"roadid": roadid})
                    s = get_real_parameter(obj_1.attrib["s"]) if "s" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"s": s})
                    t = get_real_parameter(obj_1.attrib["t"]) if "t" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"t": t})
                    orientation = self.get_Orientation(obj_1)
                    ret["params"].update({"orientation": orientation})

                elif obj_1.tag == "RelativeRoadPosition":
                    ret["type"] = "relativeroadposition"
                    ret["params"] = {}
                    entityref = get_real_parameter(obj_1.attrib["entityRef"])
                    ret["params"].update({"entityref": entityref})
                    ds = get_real_parameter(obj_1.attrib["ds"]) if "ds" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"ds": ds})
                    dt = get_real_parameter(obj_1.attrib["dt"]) if "dt" in list(obj_1.attrib.keys()) else "0.0"
                    ret["params"].update({"dt": dt})
                    orientation = self.get_Orientation(obj_1)
                    ret["params"].update({"orientation": orientation})

                else:
                    logging.error("wrong position type")
        except Exception as e:
            logging.error("generate position failed because of exception: {}".format(e))
            return {}
        return ret


class TriggerGenerator(object):
    """
    class for convert xosc event starttrigger to json.
    """
    def __init__(self):
        pass

    def generate_triggering_entities(self, obj):
        """
        @param obj: elementtree node of ByEntityCondition
        @type obj: elementtree
        @return: a dict structure of given ByEntityCondition
        @rtype: dict
        """
        ret = {}
        try:
            ret["rule"] = get_real_parameter(obj.find("TriggeringEntities").attrib["triggeringEntitiesRule"])
            ret["entityreflist"] = []
            for obj_2 in obj.find("TriggeringEntities"):
                ret["entityreflist"].append({"entityref": get_real_parameter(obj_2.attrib["entityRef"])})
        except Exception as e:
            logging.error("generate triggering entities failed because of exception: {}".format(e))
            return {}
        return ret

    def generate_by_entity_condition(self, obj, edge, delay):
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
        ret = {}
        ret["params"] = {"value": "", "freespace": "", "alongroute": "", "delay": "",
                         "conditionedge": "", "position": {}, "duration": "", "tolerance": "",
                         "triggeringentities": {"rule": "", "entityreflist": []}}
        try:
            triggeringentities = self.generate_triggering_entities(obj)
            for obj_1 in obj.find("EntityCondition"):
                if obj_1.tag == "DistanceCondition":
                    ret["type"] = "distancecondition"
                    position_generater = PositionGenerator()
                    ret["params"] = {"value": get_real_parameter(obj_1.attrib["value"]),
                                     "rule": get_real_parameter(obj_1.attrib["rule"]),
                                     "alongroute": get_real_parameter(obj_1.attrib["alongRoute"]),
                                     "freespace": get_real_parameter(obj_1.attrib["freespace"]),
                                     "conditionedge": edge, "delay": delay, "triggeringentities": triggeringentities,
                                     "position": position_generater.generate(obj_1.find("Position"))}

                if obj_1.tag == "RelativeDistanceCondition":
                    ret["type"] = "relativedistancecondition"
                    ret["params"] = {"value": get_real_parameter(obj_1.attrib["value"]),
                                     "rule": get_real_parameter(obj_1.attrib["rule"]),
                                     "freespace": get_real_parameter(obj_1.attrib["freespace"]),
                                     "entityref": get_real_parameter(obj_1.attrib["entityRef"]),
                                     "relativedistancetype": get_real_parameter(obj_1.attrib["relativeDistanceType"]),
                                     "conditionedge": edge, "delay": delay, "triggeringentities": triggeringentities}

                if obj_1.tag == "TraveledDistanceCondition":
                    ret["type"] = "traveleddistancecondition"
                    ret["params"] = {"value": get_real_parameter(obj_1.attrib["value"]), "conditionedge": edge,
                                     "delay": delay, "triggeringentities": triggeringentities}

                if obj_1.tag == "AccelerationCondition":
                    ret["type"] = "accelerationcondition"
                    ret["params"] = {"value": get_real_parameter(obj_1.attrib["value"]),
                                     "rule": get_real_parameter(obj_1.attrib["rule"]),
                                     "triggeringentities": triggeringentities, "conditionedge": edge, "delay": delay}

                if obj_1.tag == "EndOfRoadCondition":
                    ret["type"] = "endofroadcondition"
                    ret["params"] = {"duration": get_real_parameter(obj_1.attrib["duration"]),
                                     "triggeringentities": triggeringentities, "conditionedge": edge, "delay": delay}

                if obj_1.tag == "OffroadCondition":
                    ret["type"] = "offroadcondition"
                    ret["params"] = {"duration": get_real_parameter(obj_1.attrib["duration"]), "conditionedge": edge,
                                     "delay": delay, "triggeringentities": triggeringentities}

                if obj_1.tag == "ReachPositionCondition":
                    ret["type"] = "reachpositioncondition"
                    position_generater = PositionGenerator()
                    ret["params"] = {"tolerance": get_real_parameter(obj_1.attrib["tolerance"]),
                                     "triggeringentities": triggeringentities,
                                     "position": position_generater.generate(obj_1.find("Position")),
                                     "conditionedge": edge, "delay": delay}

                if obj_1.tag == "RelativeSpeedCondition":
                    ret["type"] = "relativespeedcondition"
                    ret["params"] = {"value": get_real_parameter(obj_1.attrib["value"]),
                                     "rule": get_real_parameter(obj_1.attrib["rule"]),
                                     "entityref": get_real_parameter(obj_1.attrib["entityRef"]),
                                     "triggeringentities": triggeringentities, "conditionedge": edge, "delay": delay}

                if obj_1.tag == "SpeedCondition":
                    ret["type"] = "speedcondition"
                    ret["params"] = {"value": get_real_parameter(obj_1.attrib["value"]),
                                     "rule": get_real_parameter(obj_1.attrib["rule"]),
                                     "triggeringentities": triggeringentities, "conditionedge": edge, "delay": delay}

                if obj_1.tag == "StandStillCondition":
                    ret["type"] = "standstillcondition"
                    ret["params"] = {"duration": get_real_parameter(obj_1.attrib["duration"]), "conditionedge": edge,
                                     "delay": delay, "triggeringentities": triggeringentities}

                if obj_1.tag == "TimeHeadwayCondition":
                    ret["type"] = "timeheadwaycondition"
                    ret["params"] = {"value": get_real_parameter(obj_1.attrib["value"]),
                                     "rule": get_real_parameter(obj_1.attrib["rule"]),
                                     "freespace": get_real_parameter(obj_1.attrib["freespace"]),
                                     "alongroute": get_real_parameter(obj_1.attrib["alongRoute"]),
                                     "entityref": get_real_parameter(obj_1.attrib["entityRef"]),
                                     "triggeringentities": triggeringentities, "conditionedge": edge, "delay": delay}

                if obj_1.tag == "TimeToCollisionCondition":
                    ret["type"] = "timetocollisioncondition"
                    if obj_1.find("TimeToCollisionConditionTarget").find("EntityRef") is not None:
                        ret["params"] = {"value": get_real_parameter(obj_1.attrib["value"]),
                                         "rule": get_real_parameter(obj_1.attrib["rule"]),
                                         "freespace": get_real_parameter(obj_1.attrib["freespace"]),
                                         "alongroute": get_real_parameter(obj_1.attrib["alongRoute"]),
                                         "entityref": get_real_parameter(
                                             obj_1.find("TimeToCollisionConditionTarget").find("EntityRef").attrib[
                                                 "entityRef"]),
                                         "triggeringentities": triggeringentities, "conditionedge": edge,
                                         "delay": delay, "conditiontarget": "entity"}
                    if obj_1.find("TimeToCollisionConditionTarget").find("Position") is not None:
                        position_generater = PositionGenerator()
                        ret["params"] = {"value": get_real_parameter(obj_1.attrib["value"]),
                                         "rule": get_real_parameter(obj_1.attrib["rule"]),
                                         "freespace": get_real_parameter(obj_1.attrib["freespace"]),
                                         "alongroute": get_real_parameter(obj_1.attrib["alongRoute"]),
                                         "position": position_generater.generate(
                                             obj_1.find("TimeToCollisionConditionTarget").find("Position")),
                                         "triggeringentities": triggeringentities, "conditionedge": edge,
                                         "delay": delay, "conditiontarget": "position"}


                if obj_1.tag == "CollisionCondition":
                    ret["type"] = "collisioncondition"
                    if obj_1.find("EntityRef") != None:
                        ret["params"] = {"entityref": get_real_parameter(obj_1.find("EntityRef").attrib["entityRef"]),
                                         "entitychoice": "entity", "triggeringentities": triggeringentities,
                                         "conditionedge": edge, "delay": delay}

                    if obj_1.find("ByType") != None:
                        ret["params"] = {"bytype": get_real_parameter(obj_1.find("ByType").attrib["type"]),
                                         "entitychoice": "type", "triggeringentities": triggeringentities,
                                         "conditionedge": edge, "delay": delay}
        except Exception as e:
            logging.error("generate byentitycondition failed because of exception: {}".format(e))
            return {}
        return ret

    def generate_by_value_condition(self, obj, edge, delay):
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
        ret = {}
        ret["params"] = {"value": "", "freespace": "", "alongroute": "", "delay": "",
                         "conditionedge": "", "position": {}, "duration": "", "tolerance": "",
                         "triggeringentities": {"rule": "", "entityreflist": []}}
        try:
            for obj_1 in obj:
                if obj_1.tag == "SimulationTimeCondition":
                    ret["type"] = "simulationtimecondition"
                    ret["params"] = {"value": get_real_parameter(obj_1.attrib["value"]),
                                     "rule": get_real_parameter(obj_1.attrib["rule"]),
                                     "conditionedge": edge, "delay": delay}

                if obj_1.tag == "TimeOfDayCondition":
                    ret["type"] = "timeofdaycondition"
                    ret["params"] = {"datetime": get_real_parameter(obj_1.attrib["dateTime"]),
                                     "rule": get_real_parameter(obj_1.attrib["rule"]),
                                     "conditionedge": edge, "delay": delay}

                if obj_1.tag == "TrafficSignalCondition":
                    ret["type"] = "trafficsignalcondition"
                    ret["params"] = {"name": obj_1.attrib["name"].split("id=")[1],
                                     "x": "0", "y": "0",
                                     "state": obj_1.attrib["state"],
                                     "conditionedge": edge, "delay": delay}

                if obj_1.tag == "ParameterCondition":
                    ret["type"] = "parametercondition"
                    ret["params"] = {"value": get_real_parameter(obj_1.attrib["value"]),
                                     "rule": get_real_parameter(obj_1.attrib["rule"]),
                                     "parameterref": get_real_parameter(obj_1.attrib["parameterRef"]),
                                     "conditionedge": edge, "delay": delay}
        except Exception as e:
            logging.error("generate byvaluecondition failed because of exception: {}".format(e))
            return {}
        return ret

    def generate(self, obj):
        """
        @param obj: elementtree node of Event
        @type obj: elementtree
        @return: a list structure of given Event StartTrigger
        @rtype: list
        """
        ret = []
        try:
            for obj_1 in obj.find("StartTrigger"):
                if obj_1.tag == "ConditionGroup":#ConditionGroup level
                    one_ret = []
                    for obj_2 in obj_1:
                        if obj_2.tag == "Condition":#Condition level
                            if obj_2.find("ByEntityCondition") != None:
                                one_ret.append(self.generate_by_entity_condition(
                                    obj_2.find("ByEntityCondition"), get_real_parameter(obj_2.attrib["conditionEdge"]),
                                    get_real_parameter(obj_2.attrib["delay"])))
                            if obj_2.find("ByValueCondition") != None:
                                one_ret.append(self.generate_by_value_condition(
                                    obj_2.find("ByValueCondition"), get_real_parameter(obj_2.attrib["conditionEdge"]),
                                    get_real_parameter(obj_2.attrib["delay"])))
                    ret.append(one_ret)
        except Exception as e:
            logging.error("TriggerGenerator generate function failed because of exception: {}".format(e))
            return []
        return ret


class ActionGenerator(object):
    """
    class for convert xosc event action to json.
    """
    def __init__(self):
        pass

    def generate(self, obj):
        """
        @param obj: elementtree node of Event
        @type obj: elementtree
        @return: a list structure of given Event Action
        @rtype: list
        """
        ret = []
        try:
            for obj_1 in obj:
                if obj_1.tag == "Action":
                    if obj_1.find("PrivateAction") is not None:
                        for obj_2 in obj_1.find("PrivateAction"):
                            one_ret = {}
                            ###
                            one_ret["params"] = {"name": "", "closed": "", "shape": [], "waypoint": [], "timerederence": {},
                                                 "targetspeed": {}, "transitiondynamics": {}, "position": {},
                                                 "targetlaneoffset": "undefined",
                                                 "targetlane": {}, "entityref": "", "distance": "false", "timegap": "false",
                                                 "freespace": "", "continuous": "", "dynamicconstraints": {},
                                                 "laneoffsetactiondynamics": {"maxlateralacc": "undefined"},
                                                 "laneoffsettarget": {"params": {"value": "undefined", "entityref": ""}},
                                                 "targetpositionmaster": {}, "targetposition": {},
                                                 "finalspeed": {"params": {"value": "undefined"}}}
                            ###
                            if obj_2.tag == "LongitudinalAction":
                                if obj_2.find("SpeedAction") != None:
                                    one_ret["type"] = "speedaction"
                                    one_ret["params"] = {}
                                    speed_generator = SpeedGenerator()
                                    one_ret["params"]["targetspeed"] = speed_generator.generate(
                                        obj_2.find("SpeedAction").find("SpeedActionTarget"))
                                    one_ret["params"]["transitiondynamics"] = {
                                        "dynamicsshape": get_real_parameter(
                                            obj_2.find("SpeedAction").find("SpeedActionDynamics").attrib["dynamicsShape"]),
                                        "dynamicsdimension": get_real_parameter(
                                            obj_2.find("SpeedAction").find("SpeedActionDynamics").attrib[
                                                "dynamicsDimension"]),
                                        "value": get_real_parameter(
                                            obj_2.find("SpeedAction").find("SpeedActionDynamics").attrib["value"])}

                                if obj_2.find("LongitudinalDistanceAction") != None:
                                    one_ret["type"] = "longitudinaldistanceaction"
                                    if "distance" in list(obj_2.find("LongitudinalDistanceAction").attrib.keys()):
                                        distance = get_real_parameter(
                                            obj_2.find("LongitudinalDistanceAction").attrib["distance"])
                                        one_ret["params"].update({"entityref": get_real_parameter(
                                            obj_2.find("LongitudinalDistanceAction").attrib["entityRef"]),
                                            "distance": distance,
                                            "freespace": get_real_parameter(
                                                obj_2.find("LongitudinalDistanceAction").attrib["freespace"]),
                                            "continuous": get_real_parameter(
                                                obj_2.find("LongitudinalDistanceAction").attrib["continuous"])})
                                    if "timeGap" in list(obj_2.find("LongitudinalDistanceAction").attrib.keys()):
                                        timegap = get_real_parameter(
                                            obj_2.find("LongitudinalDistanceAction").attrib["timeGap"])
                                        one_ret["params"].update({"entityref": get_real_parameter(
                                            obj_2.find("LongitudinalDistanceAction").attrib["entityRef"]),
                                            "timegap": timegap,
                                            "freespace": get_real_parameter(
                                                obj_2.find("LongitudinalDistanceAction").attrib["freespace"]),
                                            "continuous": get_real_parameter(
                                                obj_2.find("LongitudinalDistanceAction").attrib["continuous"])})

                            if obj_2.tag == "LateralAction":
                                if obj_2.find("LaneChangeAction") != None:
                                    one_ret["type"] = "lanechangeaction"
                                    one_ret["params"] = {}
                                    if "targetLaneOffset" in list(obj_2.find("LaneChangeAction").attrib):
                                        one_ret["params"]["targetlaneoffset"] = get_real_parameter(
                                            obj_2.find("LaneChangeAction").attrib["targetLaneOffset"])
                                    if obj_2.find("LaneChangeAction").find("LaneChangeTarget").find(
                                            "RelativeTargetLane") != None:
                                        one_ret["params"]["targetlane"] = {"type": "relative",
                                                                           "params": {"entityref": get_real_parameter(
                                                                               obj_2.find("LaneChangeAction").find(
                                                                                   "LaneChangeTarget").find(
                                                                                   "RelativeTargetLane").attrib[
                                                                                   "entityRef"]),
                                                                                      "value": get_real_parameter(
                                                                                          obj_2.find(
                                                                                              "LaneChangeAction").find(
                                                                                              "LaneChangeTarget").find(
                                                                                              "RelativeTargetLane").attrib[
                                                                                              "value"])}}
                                    if obj_2.find("LaneChangeAction").find("LaneChangeTarget").find(
                                                "AbsoluteTargetLane") != None:
                                        one_ret["params"]["targetlane"] = {"type": "absolute",
                                                                           "params": {"laneid": get_real_parameter(
                                                                               obj_2.find("LaneChangeAction").find(
                                                                                   "LaneChangeTarget").find(
                                                                                   "AbsoluteTargetLane").attrib["value"])}}
                                    one_ret["params"]["transitiondynamics"] = {
                                        "dynamicsshape": get_real_parameter(
                                            obj_2.find("LaneChangeAction").find("LaneChangeActionDynamics").attrib[
                                                "dynamicsShape"]),
                                        "dynamicsdimension": get_real_parameter(
                                            obj_2.find("LaneChangeAction").find("LaneChangeActionDynamics").attrib[
                                                "dynamicsDimension"]),
                                        "value": get_real_parameter(
                                            obj_2.find("LaneChangeAction").find("LaneChangeActionDynamics").attrib[
                                                "value"])}

                                if obj_2.find("LaneOffsetAction") != None:
                                    one_ret["type"] = "laneoffsetaction"
                                    one_ret["params"] = {}
                                    one_ret["params"]["continuous"] = get_real_parameter(
                                        obj_2.find("LaneOffsetAction").attrib["continuous"])
                                    one_ret["params"]["laneoffsetactiondynamics"] = {"maxlateralacc": get_real_parameter(
                                        obj_2.find("LaneOffsetAction").find("LaneOffsetActionDynamics").attrib[
                                            "maxLateralAcc"]),
                                                                                     "dynamicsshape": get_real_parameter(
                                                                                         obj_2.find(
                                                                                             "LaneOffsetAction").find(
                                                                                             "LaneOffsetActionDynamics").attrib[
                                                                                             "dynamicsShape"])}
                                    if obj_2.find("LaneOffsetAction").find("LaneOffsetTarget").find(
                                            "RelativeTargetLaneOffset") != None:
                                        one_ret["params"]["laneoffsettarget"] = {"type": "relative", "params": {
                                            "value": get_real_parameter(
                                                obj_2.find("LaneOffsetAction").find("LaneOffsetTarget").find(
                                                    "RelativeTargetLaneOffset").attrib["value"]),
                                            "entityref": get_real_parameter(
                                                obj_2.find("LaneOffsetAction").find("LaneOffsetTarget").find(
                                                    "RelativeTargetLaneOffset").attrib["entityRef"])}}
                                    if obj_2.find("LaneOffsetAction").find("LaneOffsetTarget").find(
                                                "AbsoluteTargetLaneOffset") != None:
                                        one_ret["params"]["laneoffsettarget"] = {"type": "absolute", "params": {
                                            "value": get_real_parameter(
                                                obj_2.find("LaneOffsetAction").find("LaneOffsetTarget").find(
                                                    "AbsoluteTargetLaneOffset").attrib["value"])}}

                                if obj_2.find("LateralDistanceAction") != None:
                                    one_ret["type"] = "lateraldistanceaction"
                                    one_ret["params"] = {"entityref": get_real_parameter(
                                        obj_2.find("LateralDistanceAction").attrib["entityRef"]),
                                                         "distance": get_real_parameter(
                                                             obj_2.find("LateralDistanceAction").attrib["distance"]),
                                                         "freespace": get_real_parameter(
                                                             obj_2.find("LateralDistanceAction").attrib["freespace"]),
                                                         "continuous": get_real_parameter(
                                                             obj_2.find("LateralDistanceAction").attrib["continuous"])}
                                    if obj_2.find("LateralDistanceAction").find("DynamicConstraints") != None:
                                        one_ret["params"]["dynamicconstraints"] = {"maxacceleration": get_real_parameter(
                                            obj_2.find("LateralDistanceAction").find("DynamicConstraints").attrib[
                                                "maxAcceleration"]),
                                                                                   "maxdeceleration": get_real_parameter(
                                                                                       obj_2.find(
                                                                                           "LateralDistanceAction").find(
                                                                                           "DynamicConstraints").attrib[
                                                                                           "maxDeceleration"]),
                                                                                   "maxspeed": get_real_parameter(
                                                                                       obj_2.find(
                                                                                           "LateralDistanceAction").find(
                                                                                           "DynamicConstraints").attrib[
                                                                                           "maxSpeed"])}


                            if obj_2.tag == "SynchronizeAction":
                                one_ret["type"] = "synchronizeaction"
                                position_generater_master = PositionGenerator()
                                position_generater_target = PositionGenerator()
                                if obj_2.find("FinalSpeed").find("AbsoluteSpeed") != None:
                                    one_ret["params"] = {
                                        "masterentityref": get_real_parameter(obj_2.attrib["masterEntityRef"]),
                                        "targetpositionmaster": position_generater_master.generate(
                                            obj_2.find("TargetPositionMaster")),
                                        "targetposition": position_generater_target.generate(obj_2.find("TargetPosition")),
                                        "finalspeed": {"type": "absolutespeed", "params": {"value": get_real_parameter(
                                            obj_2.find("FinalSpeed").find("AbsoluteSpeed").attrib["value"])}}}
                                if obj_2.find("FinalSpeed").find("RelativeSpeedToMaster") != None:
                                    one_ret["params"] = {
                                        "masterentityref": get_real_parameter(obj_2.attrib["masterEntityRef"]),
                                        "targetpositionmaster": position_generater_master.generate(
                                            obj_2.find("TargetPositionMaster")),
                                        "targetposition": position_generater_target.generate(obj_2.find("TargetPosition")),
                                        "finalspeed": {"type": "relativespeedtomaster",
                                                       "params": {"value": get_real_parameter(
                                                           obj_2.find("FinalSpeed").find("RelativeSpeedToMaster").attrib[
                                                               "value"]),
                                                                  "speedtargetvaluetype": get_real_parameter(
                                                                      obj_2.find("FinalSpeed").find(
                                                                          "RelativeSpeedToMaster").attrib[
                                                                          "speedTargetValueType"])}}}

                            if obj_2.tag == "RoutingAction":
                                if obj_2.find("AssignRouteAction") != None:
                                    one_ret["type"] = "assignrouteaction"
                                    waypoint_list = []
                                    for obj_3 in obj_2.find("AssignRouteAction").find("Route"):
                                        each_ret = {}
                                        each_ret["params"] = {}
                                        position_generater = PositionGenerator()
                                        each_ret["params"]["position"] = position_generater.generate(obj_3.find("Position"))
                                        waypoint_list.append(each_ret)
                                    one_ret["params"] = {"name": get_real_parameter(
                                        obj_2.find("AssignRouteAction").find("Route").attrib["name"]),
                                                         "closed": get_real_parameter(
                                                             obj_2.find("AssignRouteAction").find("Route").attrib[
                                                                 "closed"]),
                                                         "waypoint": waypoint_list}

                                if obj_2.find("FollowTrajectoryAction") != None:
                                    one_ret["type"] = "followtrajectoryaction"
                                    vertex_list = []
                                    for obj_3 in obj_2.find("FollowTrajectoryAction").find("Trajectory").find("Shape").find("Polyline"):
                                        if obj_3.tag == "Vertex":
                                            each_ret = {}
                                            each_ret["params"] = {}
                                            each_ret["time"] = get_real_parameter(obj_3.attrib["time"])
                                            position_generater = PositionGenerator()
                                            each_ret["params"]["position"] = position_generater.generate(obj_3.find("Position"))
                                            vertex_list.append(each_ret)
                                    if obj_2.find("FollowTrajectoryAction").find("TimeReference").find("None") != None:
                                        one_ret["params"] = {
                                            "name": get_real_parameter(
                                                obj_2.find("FollowTrajectoryAction").find("Trajectory").attrib["name"]),
                                            "closed": get_real_parameter(
                                                obj_2.find("FollowTrajectoryAction").find("Trajectory").attrib["closed"]),
                                            "shape": vertex_list, "timerederence": {"type": "none", "params": {
                                                "domainabsoluterelative": "absolute", "offset": "0", "scale": "1"}}}
                                    if obj_2.find("FollowTrajectoryAction").find("TimeReference").find("Timing") != None:
                                        one_ret["params"] = {
                                            "name": get_real_parameter(
                                                obj_2.find("FollowTrajectoryAction").find("Trajectory").attrib["name"]),
                                            "closed": get_real_parameter(
                                                obj_2.find("FollowTrajectoryAction").find("Trajectory").attrib["closed"]),
                                            "shape": vertex_list,
                                            "timerederence": {"type": "timing", "params": {"domainabsoluterelative":
                                                                                               get_real_parameter(
                                                                                                   obj_2.find(
                                                                                                       "FollowTrajectoryAction").find(
                                                                                                       "TimeReference").find(
                                                                                                       "Timing").attrib[
                                                                                                       "domainAbsoluteRelative"]),
                                                                                           "scale": get_real_parameter(
                                                                                               obj_2.find(
                                                                                                   "FollowTrajectoryAction").find(
                                                                                                   "TimeReference").find(
                                                                                                   "Timing").attrib[
                                                                                                   "scale"]),
                                                                                           "offset": get_real_parameter(
                                                                                               obj_2.find(
                                                                                                   "FollowTrajectoryAction").find(
                                                                                                   "TimeReference").find(
                                                                                                   "Timing").attrib[
                                                                                                   "offset"])}}}

                                if obj_2.find("AcquirePositionAction") != None:
                                    one_ret["type"] = "acquirepositionaction"
                                    position_generater = PositionGenerator()
                                    one_ret["params"] = {"position": position_generater.generate(obj_2.find("AcquirePositionAction").find("Position"))}

                            if obj_2.tag == "TeleportAction":
                                one_ret["type"] = "teleportaction"
                                position_generater = PositionGenerator()
                                one_ret["params"] = {"position": position_generater.generate(obj_2.find("Position"))}
                    if obj_1.find("GlobalAction") is not None:
                        for obj_2 in obj_1.find("GlobalAction"):
                            one_ret = {}
                            ###
                            one_ret["params"] = {"name": "", "closed": "", "shape": [], "waypoint": [],
                                                 "timerederence": {},
                                                 "targetspeed": {}, "transitiondynamics": {}, "position": {},
                                                 "targetlaneoffset": "undefined",
                                                 "targetlane": {}, "entityref": "", "distance": "", "timegap": "",
                                                 "freespace": "", "continuous": "", "dynamicconstraints": {},
                                                 "laneoffsetactiondynamics": {"maxlateralacc": "undefined"},
                                                 "laneoffsettarget": {
                                                     "params": {"value": "undefined", "entityref": ""}},
                                                 "targetpositionmaster": {}, "targetposition": {},
                                                 "finalspeed": {"params": {"value": "undefined"}}}
                            ###
                            if obj_2.tag == "InfrastructureAction":
                                if obj_2.find("TrafficSignalAction") != None:
                                    if obj_2.find("TrafficSignalAction").find("TrafficSignalStateAction") != None:
                                        one_ret["type"] = "trafficsignalstateaction"
                                        one_ret["params"]["name"] = \
                                            obj_2.find("TrafficSignalAction").find("TrafficSignalStateAction").attrib[
                                                "name"].split("id=")[1]
                                        one_ret["params"]["x"] = "0"
                                        one_ret["params"]["y"] = "0"
                                        one_ret["params"]["state"] = \
                                            obj_2.find("TrafficSignalAction").find("TrafficSignalStateAction").attrib[
                                                "state"]
                    ret.append(one_ret)
        except Exception as e:
            logging.error("ActionGenerator generate function failed because of exception: {}".format(e))
            return []
        return ret


class SpeedGenerator(object):
    """
    class for convert xosc speed to json.
    """
    def __init__(self):
        pass

    def generate(self, obj):
        """
        @param obj: elementtree node of TargetSpeed
        @type obj: elementtree
        @return: a dict structure of given TargetSpeed
        @rtype: dict
        """
        ret = {}
        try:
            for obj_1 in obj:
                if obj_1.tag == "AbsoluteTargetSpeed":
                    ret["type"] = "absolute"
                    ret["params"] = {"value": get_real_parameter(obj_1.attrib["value"])}
                if obj_1.tag == "RelativeTargetSpeed":
                    ret["type"] = "relative"
                    ret["params"] = {"value": get_real_parameter(obj_1.attrib["value"]),
                                     "entityref": get_real_parameter(obj_1.attrib["entityRef"]),
                                     "valuetype": get_real_parameter(obj_1.attrib["speedTargetValueType"]),
                                     "continuous": get_real_parameter(obj_1.attrib["entityRef"])}
        except Exception as e:
            logging.error("generate speed failed because of exception: {}".format(e))
            return {}
        return ret


class OuterXoscDeserializer(object):
    def __init__(self, filename):
        """
        @param filename: xosc file path
        @type filename: str
        """
        self.json_dict = {}
        self.json_dict["basic"] = {}
        self.json_dict["init_environment"] = {}
        self.json_dict["eval_conditions"] = {}#new criteria do not need this
        self.json_dict["init_entities"] = []
        self.json_dict["triggers_actions"] = []
        self.filename = filename

    def get_ParameterDeclaration(self, obj):
        if obj.find("ParameterDeclarations") is None:
            return
        for obj_1 in obj.find("ParameterDeclarations"):
            paramerter_declaration_dict.update({obj_1.attrib["name"]: obj_1.attrib["value"]})
        if obj.find("Storyboard").find("Init").find("ParameterDeclarations") is not None:
            for obj_1 in obj.find("Storyboard").find("Init").find("ParameterDeclarations"):
                paramerter_declaration_dict.update({obj_1.attrib["name"]: obj_1.attrib["value"]})
        if obj.find("Storyboard").find("Story").find("ParameterDeclarations") is not None:
            for obj_1 in obj.find("Storyboard").find("Story").find("ParameterDeclarations"):
                paramerter_declaration_dict.update({obj_1.attrib["name"]: obj_1.attrib["value"]})
        return

    def deserialize_FileHeader(self, obj):
        """
        @param obj: elementtree node of FileHeader
        @type obj: elementtree
        @return: update self.json_dict
        @rtype:
        """
        try:
            self.json_dict["basic"]["description"] = obj.attrib["description"]
            self.json_dict["basic"]["traffic"] = "false"
        except Exception as e:
            logging.error("deserialize_FileHeader function failed because of exception: {}".format(e))

    def deserialize_RoadNetwork(self, obj):
        """
        @param obj: elementtree node of RoadNetwork
        @type obj: elementtree
        @return: update self.json_dict
        @rtype:
        """
        try:
            for obj_1 in obj:
                if obj_1.tag == "LogicFile":
                    self.json_dict["basic"]["xodr"] = get_real_parameter(obj_1.attrib["filepath"])
        except Exception as e:
            logging.error("deserialize_RoadNetwork function failed because of exception: {}".format(e))

    def deserialize_Entities(self, obj):
        """
        @param obj: elementtree node of RoadNetwork
        @type obj: elementtree
        @return: update self.json_dict
        @rtype:
        """
        try:
            for obj_1 in obj:
                if obj_1.tag == "ScenarioObject":
                    name = get_real_parameter(obj_1.attrib["name"])
                    if "ego" in name.lower():
                        self.json_dict["init_entities"].append({"name": "ego_vehicle", "type": "vehicle"})
                        continue

                    for obj_2 in obj_1:
                        if obj_2.tag == "Vehicle":
                            v = get_real_parameter(obj_2.attrib["vehicleCategory"])
                            if v == "car":
                                self.json_dict["init_entities"].append({"name": name, "type": "vehicle", "model": "vehicle.tesla.model3"})
                            if v == "van":
                                self.json_dict["init_entities"].append({"name": name, "type": "vehicle", "model": "vehicle.volkswagen.t2_2021"})
                            if v == "truck":
                                self.json_dict["init_entities"].append({"name": name, "type": "vehicle", "model": "vehicle.carlamotors.firetruck"})
                            if v == "motorbike":
                                self.json_dict["init_entities"].append({"name": name, "type": "vehicle", "model": "vehicle.harley-davidson.low_rider"})
                            if v == "bicycle":
                                self.json_dict["init_entities"].append({"name": name, "type": "nonvehicle", "model": "vehicle.bh.crossbike"})

                        if obj_2.tag == "Pedestrian":
                            self.json_dict["init_entities"].append({"name": name, "type": "pedestrian", "model": "walker.pedestrian.0001"})
        except Exception as e:
            logging.error("deserialize_Entities function failed because of exception: {}".format(e))

    def convert_rad_to_angle(self, rad):
        """
        @param angle: position hpr rad
        @type angle: str
        @return: position hpr angle
        @rtype: str
        """
        return str(float(rad) / math.pi * 180)

    def get_init_environment(self, obj):
        """
        @param obj: elementtree node of Environment
        @type obj: elementtree
        @return: update self.json_dict
        @rtype:
        """
        self.json_dict["init_environment"]["weather"] = {}
        self.json_dict["init_environment"]["weather"]["cloudness"] = "10"
        self.json_dict["init_environment"]["weather"]["precipitation_deposits"] = "0"
        self.json_dict["init_environment"]["weather"]["wind_intensity"] = "10"
        self.json_dict["init_environment"]["weather"]["fog_density"] = "10"
        self.json_dict["init_environment"]["weather"]["fog_distance"] = "75"
        self.json_dict["init_environment"]["weather"]["wetness"] = "0"
        self.json_dict["init_environment"]["weather"]["fog_falloff"] = "1"
        self.json_dict["init_environment"]["weather"]["sky_visibility"] = "true"
        self.json_dict["init_environment"]["weather"]["fog_visualrange"] = get_real_parameter(
            obj.find("Weather").find("Fog").attrib["visualRange"])
        self.json_dict["init_environment"]["weather"]["precipitation"] = get_real_parameter(
            obj.find("Weather").find("Precipitation").attrib["intensity"])
        self.json_dict["init_environment"]["weather"]["cloudstate"] = get_real_parameter(
            obj.find("Weather").attrib["cloudState"])
        self.json_dict["init_environment"]["weather"]["sun_azimuth_angle"] = self.convert_rad_to_angle(
            get_real_parameter(obj.find("Weather").find("Sun").attrib["azimuth"]))
        self.json_dict["init_environment"]["weather"]["sun_altitude_angle"] = self.convert_rad_to_angle(
            get_real_parameter(obj.find("Weather").find("Sun").attrib["elevation"]))

    def get_eval_conditions(self, obj):
        """
        @param obj: elementtree node of Criteria ConditionGroup
        @type obj: elementtree
        @return: update self.json_dict
        @rtype:
        """
        for obj_1 in obj:
            if obj_1.attrib["name"] == "criteria_MaxVelocityTest":
                self.json_dict["eval_conditions"]["max_velocity_test"] = obj_1.find("ByValueCondition").find("ParameterCondition").attrib["value"]
                self.json_dict["eval_conditions"]["tick_max_velocity_test"] = "true"
            if obj_1.attrib["name"] == "criteria_CollisionTest":
                self.json_dict["eval_conditions"]["collision_test"] = "true"
            if obj_1.attrib["name"] == "criteria_DrivenDistanceTest":
                self.json_dict["eval_conditions"]["agent_block_test"] = "true"
            if obj_1.attrib["name"] == "criteria_KeepLaneTest":
                self.json_dict["eval_conditions"]["keep_lane_test"] = "true"
            if obj_1.attrib["name"] == "criteria_OffRoadTest":
                self.json_dict["eval_conditions"]["off_road_test"] = "true"
            if obj_1.attrib["name"] == "criteria_OnSidewalkTest":
                self.json_dict["eval_conditions"]["on_sidewalk_test"] = "true"
            if obj_1.attrib["name"] == "criteria_WrongLaneTest":
                self.json_dict["eval_conditions"]["wrong_lane_test"] = "true"
            if obj_1.attrib["name"] == "criteria_RunningRedLightTest":
                self.json_dict["eval_conditions"]["running_red_light_test"] = "true"
            if obj_1.attrib["name"] == "criteria_RunningStopTest":
                self.json_dict["eval_conditions"]["running_stop_test"] = "true"
            self.json_dict["eval_conditions"]["max_longitudinal_accel_test"] = "5"
            self.json_dict["eval_conditions"]["tick_max_longitudinal_accel_test"] = "true"
            self.json_dict["eval_conditions"]["max_lateral_accel_test"] = "5"
            self.json_dict["eval_conditions"]["tick_max_lateral_accel_test"] = "true"

    def get_init_entities(self, obj):
        """
        @param obj: elementtree node of Actions
        @type obj: elementtree
        @return: update self.json_dict
        @rtype:
        """
        try:
            for obj_1 in obj:
                if obj_1.tag == "Private":
                    for ent in self.json_dict["init_entities"]:
                        if get_real_parameter(obj_1.attrib["entityRef"]) == ent["name"] or (
                                "ego" in get_real_parameter(obj_1.attrib["entityRef"]).lower() and "ego" in ent[
                            "name"]):
                            for obj_2 in obj_1:
                                if obj_2.find("TeleportAction") != None:
                                    start_position_generater = PositionGenerator()
                                    ent["start_position"] = start_position_generater.generate(
                                        obj_2.find("TeleportAction").find("Position"))
                                if obj_2.find("LongitudinalAction") != None:
                                    speed_generator = SpeedGenerator()
                                    ent["speed"] = speed_generator.generate(
                                        obj_2.find("LongitudinalAction").find("SpeedAction").find("SpeedActionTarget"))
        except Exception as e:
            logging.error("get_init_entities function failed because of exception: {}".format(e))


    def get_triggers_actions(self, obj):
        """
        @param obj: elementtree node of Story
        @type obj: elementtree
        @return: update self.json_dict
        @rtype:
        """
        try:
            for obj_1 in obj:
                if obj_1.tag == "Act":
                    for obj_2 in obj_1:
                        if obj_2.tag == "ManeuverGroup":
                            if obj_2.find("Actors").find("EntityRef") is not None:
                                actor = get_real_parameter(obj_2.find("Actors").find("EntityRef").attrib["entityRef"])
                            else:
                                actor = "None"
                            if actor == "ego_vehicle":
                                continue
                            for obj_3 in obj_2.find("Maneuver"):
                                if obj_3.tag == "Event":
                                    one_ret = {}
                                    one_ret["actor"] = actor
                                    one_ret["priority"] = obj_3.attrib["priority"]
                                    trigger_generator = TriggerGenerator()
                                    action_generator = ActionGenerator()
                                    one_ret["trigger"] = trigger_generator.generate(obj_3)
                                    one_ret["action"] = action_generator.generate(obj_3)
                                    self.json_dict["triggers_actions"].append(one_ret)
            for ent in self.json_dict["init_entities"]:
                if ent["name"] == "ego_vehicle":
                    ret = {}
                    ret["type"] = "worldposition"
                    ret["params"] = {}
                    ret["params"].update({"x": "0.0", "y": "0.0", "z": "0.0", "h": "0.0", "p": "0.0", "r": "0.0"})
                    ent["end_position"] = ret
        except Exception as e:
            logging.error("get_triggers_actions function failed because of exception: {}".format(e))

    def deserialize_Storyboard(self, obj):
        """
        @param obj: elementtree node of Storyboard
        @type obj: elementtree
        @return: update self.json_dict
        @rtype:
        """
        self.get_init_environment(obj.find("Init").find("Actions").find("GlobalAction").find("EnvironmentAction").find("Environment"))
        # self.get_eval_conditions(obj.find("StopTrigger").find("ConditionGroup"))
        self.get_init_entities(obj.find("Init").find("Actions"))
        # self.get_triggers_actions(obj.find("Story").find("Act"))
        self.get_triggers_actions(obj.find("Story"))

    def dict2json(self):
        """
        @return: save json file of generated dict
        @rtype:
        """
        # print(self.json_dict)
        return json.dumps(self.json_dict, indent=4, ensure_ascii=False)


    def deserialize(self, root):
        """
        @return:update self.json_dict
        @rtype:
        """
        # tree = ET.parse(self.filename)
        # root = tree.getroot()
        self.get_ParameterDeclaration(root)
        self.deserialize_FileHeader(root.find("FileHeader"))
        self.deserialize_RoadNetwork(root.find("RoadNetwork"))
        self.deserialize_Entities(root.find("Entities"))
        self.deserialize_Storyboard(root.find("Storyboard"))
        return self.dict2json()


# if __name__ == "__main__":
#     # filename1 = "DoubleLaneChanger-out2.xosc"
#     # filename1 = "./xosc/rpf1-uploadchange.xosc"
#     filename1 = r"E:\project\auto_drive_test\scenario\trafficsignal\test\ts-action-test-outer.xosc"
#
#     tree = ET.parse(filename1)
#     root = tree.getroot()
#     oxd = OuterXoscDeserializer(filename1)
#     oxd.deserialize(root)




