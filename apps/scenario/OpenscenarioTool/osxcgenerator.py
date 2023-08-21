#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: renpf
# datetime: 20220816

import os
from os.path import join
import xml.etree.ElementTree as ET
from .utils import *
from .scenarioobjectgenerator import ScenarioObjectGenerator
from .actiongenerator import InitActionGenerator, StoryActionGenerator
from .conditiongenerator import ConditionGenerator
from datetime import datetime
import json


class XoscGenerator:
    """
    convert json to oxsc v1.0.0.
    """

    def __init__(self, open_scenario_json, catalog_file_path, xosc_dest_path):
        """
        :param json_file_path: string. location of the ui json file.
        :param catalog_file_path: string. location of the catalog json file.
        """
        self.json_file_path = open_scenario_json
        # self.xosc_file_path = json_file_path[:-4] + "xosc"
        # self.xosc_file_path = join(os.path.dirname(__file__), "openscenario.xosc")
        self.xosc_file_path = xosc_dest_path
        self.catalog_file_path = catalog_file_path

        self.Act_seq = 1
        self.ManeuverGroup_seq = 1
        self.Maneuver_seq = 1
        self.Event_seq = 1
        self.Action_seq = 1
        self.Condition_seq = 1
        self.ConditionGroup_seq = 1
        self.previous_actor = None
        self.OpenSCENARIO = ET.Element("OpenSCENARIO")
        # self.OpenSCENARIO.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        # self.OpenSCENARIO.set("xsi:noNamespaceSchemaLocation", "OpenSCENARIO.xsd")
        # with open(self.json_file_path, 'r') as fr:
        self.json_dict = json.loads(open_scenario_json)

    @catch_exception
    def generate_whole_file(self):
        """
        :return: the xosc file path.
        """
        self.generate_FileHeader()
        self.generate_CatalogLocations()
        self.generate_RoadNetwork()
        self.generate_Entities()
        self.generate_Storyboard()

        tree = ET.ElementTree(self.OpenSCENARIO)
        pretty_xml(self.OpenSCENARIO, "\t", "\n")
        tree.write(self.xosc_file_path, encoding="UTF-8", xml_declaration=True, method="xml")
        return self.xosc_file_path

    def generate_FileHeader(self, revMajor="1", revMinor="0", author="oasis"):
        """
        :param revMajor: string. revMajor value.
        :param revMinor: string. revMinor value.
        :param date: string. time when editing the scenario.
        :param author: string. person who edits the scenario.
        :return: updating of the xsoc file.
        """
        self.FileHeader = ET.SubElement(self.OpenSCENARIO, "FileHeader")
        self.FileHeader.set("revMajor", revMajor)
        self.FileHeader.set("revMinor", revMinor)
        self.FileHeader.set("date", datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        self.FileHeader.set("description", self.json_dict["basic"]["description"])
        if self.json_dict["basic"].get("traffic") == "true":
            self.FileHeader.set("author", author+"_WT")
        else:
            self.FileHeader.set("author", author)
        return

    def generate_CatalogLocations(self):
        """
        :return: updating of the xsoc file.
        """
        CatalogLocations = ET.SubElement(self.OpenSCENARIO, "CatalogLocations")
        # VehicleCatalog = ET.SubElement(CatalogLocations, "VehicleCatalog")
        # Directory = ET.SubElement(VehicleCatalog, "Directory")
        # Directory.set("path", "Catalogs/Vehicles")
        # ControllerCatalog = ET.SubElement(CatalogLocations, "ControllerCatalog")
        # Directory = ET.SubElement(ControllerCatalog, "Directory")
        # Directory.set("path", ControllerCatalog_path)
        return

    def generate_RoadNetwork(self):
        """
        :return: updating of the xsoc file.
        """
        RoadNetwork = ET.SubElement(self.OpenSCENARIO, "RoadNetwork")
        LogicFile = ET.SubElement(RoadNetwork, "LogicFile")
        LogicFile.set("filepath", self.json_dict["basic"]["xodr"])
        return

    def generate_Entities(self):
        """
        :return: updating of the xsoc file.
        """
        Entities = ET.SubElement(self.OpenSCENARIO, "Entities")
        sog = ScenarioObjectGenerator(self.catalog_file_path)
        self.all_entity_list = []
        for init_entity in self.json_dict["init_entities"]:
            self.all_entity_list.append(init_entity["name"])
            sog.generate_scenarioobject(Entities, **init_entity)
        self.all_entity_list.sort()
        return

    def generate_Storyboard(self):
        """
        :return: updating of the xsoc file.
        """
        Storyboard = ET.SubElement(self.OpenSCENARIO, "Storyboard")
        Init = ET.SubElement(Storyboard, "Init")
        Actions = ET.SubElement(Init, "Actions")
        init_ag = InitActionGenerator(Actions)
        init_ag.generate_global_action(**self.json_dict["init_environment"])#environment action only generate once
        for init_entity in self.json_dict["init_entities"]:
            init_ag.generate_private_action(**init_entity)#each init_entity location and speed
        Story = ET.SubElement(Storyboard, "Story")
        Story.set("name", "MyStory")
        # one act in story.
        # multi maneuvergroup per act(different entity).
        # one starttrigger per act.
        # one maneuver per maneuvergroup.
        # multi event per maneuver for one actor.
        # multi action per event.
        # one starttrigger per event.
        # multi conditiongroup per starttrigger.
        # multi condition per conditiongroup.
        Act = ET.SubElement(Story, "Act")
        Act.set("name", "Act" + str(self.Act_seq))
        self.Act_seq += 1
        actor_list = []
        for event in self.json_dict["triggers_actions"]:#set actor because different actor, different ManeuverGroup
            actor_list.append(event["actor"])
        actor_list_new = list(set(actor_list))
        actor_list_new.sort(key=actor_list.index)
        self.generate_ManeuverGroup_for_ego(Act, "ego_vehicle")
        for actor in actor_list_new:
            if actor != "ego_vehicle":
                self.generate_ManeuverGroup(Act, actor)# multi maneuvergroups per act for different actor.
        self.generate_Act_StartTrigger(Act)
        self.generate_Act_StopTrigger(Act)#stop scenario
        StopTrigger_criteria = ET.SubElement(Storyboard, "StopTrigger")
        # self.generate_StopTrigger_Criteria(StopTrigger_criteria, **self.json_dict["eval_conditions"])#evaluate scenario
        return

    def generate_ManeuverGroup(self, upper_object, actor):
        """
        :param upper_object: string. upper node of ManeuverGroup, is Act.
        :param seq: int. seq of actor_list.
        :param actor: string. actor name.
        :return: updating of the xsoc file.
        """
        ManeuverGroup = ET.SubElement(upper_object, "ManeuverGroup")
        ManeuverGroup.set("maximumExecutionCount", "1")
        ManeuverGroup.set("name", "ManeuverGroup" + str(self.ManeuverGroup_seq))
        self.ManeuverGroup_seq += 1
        Actors = ET.SubElement(ManeuverGroup, "Actors")
        Actors.set("selectTriggeringEntities", "false")
        if actor != "None":
            EntityRef = ET.SubElement(Actors, "EntityRef")
            EntityRef.set("entityRef", actor)
        self.generate_Maneuver(ManeuverGroup, actor)
        return

    def generate_ManeuverGroup_for_ego(self, upper_object, actor): #add controller when story begins
        """
        :param upper_object: string. upper node of ManeuverGroup, is Act.
        :param seq: int. seq of actor_list.
        :param actor: string. actor name.
        :return: updating of the xsoc file.
        """
        ManeuverGroup = ET.SubElement(upper_object, "ManeuverGroup")
        ManeuverGroup.set("maximumExecutionCount", "1")
        ManeuverGroup.set("name", "ManeuverGroup" + str(self.ManeuverGroup_seq))
        self.ManeuverGroup_seq += 1
        Actors = ET.SubElement(ManeuverGroup, "Actors")
        Actors.set("selectTriggeringEntities", "false")
        EntityRef = ET.SubElement(Actors, "EntityRef")
        EntityRef.set("entityRef", actor)
        Maneuver = ET.SubElement(ManeuverGroup, "Maneuver")  # one maneuver per maneuvergroup.
        Maneuver.set("name", "Maneuver" + str(self.Maneuver_seq))
        self.Maneuver_seq += 1
        Event = ET.SubElement(Maneuver, "Event")
        event_name = "E" + str(self.Event_seq) + "ofActor" + actor
        Event.set("name", event_name)
        self.Event_seq += 1
        Event.set("priority", "overwrite")
        ###action begin###
        Action = ET.SubElement(Event, "Action")
        action_name = "A" + str(self.Action_seq) + "of" + event_name
        Action.set("name", action_name)
        self.Action_seq += 1
        PrivateAction = ET.SubElement(Action, "PrivateAction")
        ControllerAction = ET.SubElement(PrivateAction, "ControllerAction")
        AssignControllerAction = ET.SubElement(ControllerAction, "AssignControllerAction")
        Controller = ET.SubElement(AssignControllerAction, "Controller")
        Controller.set("name", "HeroAgent")
        Properties = ET.SubElement(Controller, "Properties")
        Property = ET.SubElement(Properties, "Property")
        Property.set("name", "module")
        Property.set("value", "external_control")
        # ET.SubElement(Properties, 'Property',
        #               attrib={'name': 'module', 'value': 'carla_ros_scenario_runner.ros_vehicle_control'})
        # ET.SubElement(Properties, 'Property',
        #               attrib={'name': 'launch', 'value': 'carla_motion_control.launch'})
        # ET.SubElement(Properties, 'Property',
        #               attrib={'name': 'launch-package', 'value': 'carla_motion_control'})
        OverrideControllerValueAction = ET.SubElement(ControllerAction, "OverrideControllerValueAction")
        Throttle = ET.SubElement(OverrideControllerValueAction, "Throttle")
        Throttle.set("value", "0")
        Throttle.set("active", "false")
        Brake = ET.SubElement(OverrideControllerValueAction, "Brake")
        Brake.set("value", "0")
        Brake.set("active", "false")
        Clutch = ET.SubElement(OverrideControllerValueAction, "Clutch")
        Clutch.set("value", "0")
        Clutch.set("active", "false")
        ParkingBrake = ET.SubElement(OverrideControllerValueAction, "ParkingBrake")
        ParkingBrake.set("value", "0")
        ParkingBrake.set("active", "false")
        SteeringWheel = ET.SubElement(OverrideControllerValueAction, "SteeringWheel")
        SteeringWheel.set("value", "0")
        SteeringWheel.set("active", "false")
        Gear = ET.SubElement(OverrideControllerValueAction, "Gear")
        Gear.set("number", "0")
        Gear.set("active", "false")
        ###action finish###

        ###starttrigger begin###
        StartTrigger = ET.SubElement(Event, "StartTrigger")
        ConditionGroup = ET.SubElement(StartTrigger, "ConditionGroup")
        conditiongroup_name = "CG" + str(self.ConditionGroup_seq) + "of" + event_name
        # ConditionGroup.set("name", conditiongroup_name)
        Condition = ET.SubElement(ConditionGroup, "Condition")
        condition_name = "C" + str(self.Condition_seq) + "of" + conditiongroup_name
        Condition.set("name", condition_name)
        Condition.set("delay", "0")
        Condition.set("conditionEdge", "rising")
        ByValueCondition = ET.SubElement(Condition, "ByValueCondition")
        SimulationTimeCondition = ET.SubElement(ByValueCondition, "SimulationTimeCondition")
        SimulationTimeCondition.set("value", "0.1")#ad system take over when scenario bengin for 1 s
        SimulationTimeCondition.set("rule", "greaterThan")
        return

    def generate_Maneuver(self, upper_object, actor):
        """
        :param upper_object: string. upper node of Maneuver, is ManeuverGroup.
        :param actor: string. actor name.
        :return: updating of the xsoc file.
        """

        # one maneuver per maneuvergroup.
        Maneuver = ET.SubElement(upper_object, "Maneuver")
        Maneuver.set("name", "Maneuver" + str(self.Maneuver_seq))
        self.Maneuver_seq += 1
        # multi event per maneuver for one actor.
        for event in self.json_dict["triggers_actions"]:
            self.generate_Event(Maneuver, actor, event)
        return

    def generate_Event(self, upper_object, actor, event):
        """
        :param upper_object: string. upper node of Event, is Maneuver.
        :param actor: string. actor name.
        :param event: string. event name.
        :param event_num: int. seq of event list.
        :return: updating of the xsoc file.
        """

        if event["actor"] == actor:
            if self.previous_actor != actor:
                self.Event_seq = 1
                self.previous_actor = actor
            Event = ET.SubElement(upper_object, "Event")
            event_name = "E" + str(self.Event_seq) + "ofActor" + actor
            Event.set("name", event_name)
            self.Event_seq += 1
            Event.set("priority", event["priority"])
            self.Action_seq = 1
            for action_dict in event["action"]:  # multi action per event.
                self.generate_Action(Event, action_dict, event_name)
            StartTrigger = ET.SubElement(Event, "StartTrigger")  # one starttrigger per event.
            self.ConditionGroup_seq = 1
            for conditiongroup_list in event["trigger"]:  # multi conditiongroup per starttrigger.
                self.generate_ConditionGroup(StartTrigger, conditiongroup_list, event_name)
        return


    def generate_Action(self, upper_object, action_dict, event_name):
        """
        :param upper_object: string. upper node of Action, is Event.
        :param action_num: int. seq of action list.
        :param action_dict: dict. params of action.
        :return: updating of the xsoc file.
        """
        Action = ET.SubElement(upper_object, "Action")
        action_name = "A" + str(self.Action_seq) + "of" + event_name
        Action.set("name", action_name)
        self.Action_seq += 1
        sag = StoryActionGenerator(Action)
        sag.generate_private_action(**action_dict)
        return


    def generate_ConditionGroup(self, upper_object, conditiongroup_list, event_name):
        """
        :param upper_object: string. upper node of ConditionGroup, is StartTrigger.
        :param conditiongroup_list: list. list of conditiongroups.
        :return: updating of the xsoc file.
        """
        ConditionGroup = ET.SubElement(upper_object, "ConditionGroup")
        conditiongroup_name = "CG" + str(self.ConditionGroup_seq) + "of" + event_name
        # ConditionGroup.set("name", conditiongroup_name)
        self.ConditionGroup_seq += 1
        self.Condition_seq = 1
        for condition_dict in conditiongroup_list:  # multi condition per conditiongroup.
            self.generate_Condition(ConditionGroup, condition_dict, conditiongroup_name)
        return


    def generate_Condition(self, upper_object, condition_dict, conditiongroup_name):
        """
        :param upper_object: string. upper node of Condition, is ConditionGroup.
        :param condition_dict: dict. params of condition
        :return: updating of the xsoc file.
        """
        Condition = ET.SubElement(upper_object, "Condition")
        condition_name = "C" + str(self.Condition_seq) + "of" + conditiongroup_name
        Condition.set("name", condition_name)
        self.Condition_seq += 1
        Condition.set("delay", condition_dict["params"]["delay"])
        Condition.set("conditionEdge", condition_dict["params"]["conditionedge"])
        cg = ConditionGenerator(Condition)
        cg.generate_condition(**condition_dict)
        return

    def generate_Act_StartTrigger(self, upper_object):
        """
        :param upper_object: string. upper node of StarTtrigger, is Act.
        :return: updating of the xsoc file.
        """
        StartTrigger = ET.SubElement(upper_object, "StartTrigger")
        ConditionGroup = ET.SubElement(StartTrigger, "ConditionGroup")
        Condition = ET.SubElement(ConditionGroup, "Condition")
        Condition.set("name", "ActStartCondition")
        Condition.set("delay", "0")
        Condition.set("conditionEdge", "rising")
        param_dict = {"type": "simulationtimecondition", "params": {"value": "0", "rule": "greaterThan"}}
        cg = ConditionGenerator(Condition)
        cg.generate_condition(**param_dict)
        return

    def generate_Act_StopTrigger(self, upper_object):
        """
        :param upper_object: string. upper node of StopTrigger, is Act.
        :return: updating of the xsoc file.
        """
        StopTrigger = ET.SubElement(upper_object, "StopTrigger")
        ConditionGroup_timeout = ET.SubElement(StopTrigger, "ConditionGroup")
        Condition = ET.SubElement(ConditionGroup_timeout, "Condition")
        Condition.set("name", "timeout")
        Condition.set("delay", "0")
        Condition.set("conditionEdge", "rising")
        param_dict_timeout = {"type": "simulationtimecondition", "params": {"value": "180", "rule": "greaterThan"}}
        cg = ConditionGenerator(Condition)
        cg.generate_condition(**param_dict_timeout)

        ConditionGroup_collision = ET.SubElement(StopTrigger, "ConditionGroup")
        Condition = ET.SubElement(ConditionGroup_collision, "Condition")
        Condition.set("name", "collision_vehicle")
        Condition.set("delay", "0")
        Condition.set("conditionEdge", "rising")
        param_dict_collision_vehicle = {"type": "collisioncondition", "params": {"triggeringentities": {"rule": "any",
                                        "entityreflist": [{"entityref": "ego_vehicle"}]}, "entitychoice": "type",
                                        "bytype": "vehicle"}}
        cg = ConditionGenerator(Condition)
        cg.generate_condition(**param_dict_collision_vehicle)

        ConditionGroup_collision = ET.SubElement(StopTrigger, "ConditionGroup")
        Condition = ET.SubElement(ConditionGroup_collision, "Condition")
        Condition.set("name", "collision_pedestrian")
        Condition.set("delay", "0")
        Condition.set("conditionEdge", "rising")
        param_dict_collision_pedestrian = {"type": "collisioncondition", "params": {"triggeringentities": {"rule": "any",
                                           "entityreflist": [{"entityref": "ego_vehicle"}]}, "entitychoice": "type",
                                           "bytype": "pedestrian"}}
        cg = ConditionGenerator(Condition)
        cg.generate_condition(**param_dict_collision_pedestrian)

        ConditionGroup_collision = ET.SubElement(StopTrigger, "ConditionGroup")
        Condition = ET.SubElement(ConditionGroup_collision, "Condition")
        Condition.set("name", "collision_misobject")
        Condition.set("delay", "0")
        Condition.set("conditionEdge", "rising")
        param_dict_collision_misobject = {"type": "collisioncondition", "params": {"triggeringentities": {"rule": "any",
                                          "entityreflist": [{"entityref": "ego_vehicle"}]}, "entitychoice": "type",
                                          "bytype": "miscellaneous"}}
        cg = ConditionGenerator(Condition)
        cg.generate_condition(**param_dict_collision_misobject)

        ConditionGroup_collision = ET.SubElement(StopTrigger, "ConditionGroup")
        Condition = ET.SubElement(ConditionGroup_collision, "Condition")
        Condition.set("name", "reach_destination")
        Condition.set("delay", "0")
        Condition.set("conditionEdge", "rising")
        for item in self.json_dict["init_entities"]:
            if item["name"] == "ego_vehicle":
                ego_dict = item
        param_dict_reach_destination = {"type": "reachpositioncondition", "params": {"triggeringentities": {"rule": "any",
                                    "entityreflist": [{"entityref": "ego_vehicle"}]}, "tolerance": "8.0",
                                    "position": ego_dict["end_position"]}}
        cg = ConditionGenerator(Condition)
        cg.generate_condition(**param_dict_reach_destination)
        return

    def generate_StopTrigger_Criteria(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of ConditionGroup, is generate_StopTrigger.
        :return: updating of the xsoc file.
        """
        ConditionGroup = ET.SubElement(upper_object, "ConditionGroup")
        if kwargs["tick_max_velocity_test"] == "true":
            Condition = ET.SubElement(ConditionGroup, "Condition")
            Condition.set("name", "criteria_MaxVelocityTest")
            Condition.set("delay", "0")
            Condition.set("conditionEdge", "rising")
            ByValueCondition = ET.SubElement(Condition, "ByValueCondition")
            ParameterCondition = ET.SubElement(ByValueCondition, "ParameterCondition")
            ParameterCondition.set("parameterRef", "max_velocity_allowed")
            ParameterCondition.set("rule", "greaterThan")
            ParameterCondition.set("value", kwargs["max_velocity_test"])

        if kwargs["collision_test"] == "true":
            Condition = ET.SubElement(ConditionGroup, "Condition")
            Condition.set("name", "criteria_CollisionTest")
            Condition.set("delay", "0")
            Condition.set("conditionEdge", "rising")
            ByValueCondition = ET.SubElement(Condition, "ByValueCondition")
            ParameterCondition = ET.SubElement(ByValueCondition, "ParameterCondition")
            ParameterCondition.set("parameterRef", "")
            ParameterCondition.set("rule", "lessThan")
            ParameterCondition.set("value", "")

        if kwargs["agent_block_test"] == "true":
            Condition = ET.SubElement(ConditionGroup, "Condition")
            Condition.set("name", "criteria_DrivenDistanceTest")
            Condition.set("delay", "0")
            Condition.set("conditionEdge", "rising")
            ByValueCondition = ET.SubElement(Condition, "ByValueCondition")
            ParameterCondition = ET.SubElement(ByValueCondition, "ParameterCondition")
            ParameterCondition.set("parameterRef", "distance_success")
            ParameterCondition.set("rule", "greaterThan")
            ParameterCondition.set("value", "100")

        if kwargs["keep_lane_test"] == "true":
            Condition = ET.SubElement(ConditionGroup, "Condition")
            Condition.set("name", "criteria_KeepLaneTest")
            Condition.set("delay", "0")
            Condition.set("conditionEdge", "rising")
            ByValueCondition = ET.SubElement(Condition, "ByValueCondition")
            ParameterCondition = ET.SubElement(ByValueCondition, "ParameterCondition")
            ParameterCondition.set("parameterRef", "")
            ParameterCondition.set("rule", "lessThan")
            ParameterCondition.set("value", "")

        if kwargs["off_road_test"] == "true":
            Condition = ET.SubElement(ConditionGroup, "Condition")
            Condition.set("name", "criteria_OffRoadTest")
            Condition.set("delay", "0")
            Condition.set("conditionEdge", "rising")
            ByValueCondition = ET.SubElement(Condition, "ByValueCondition")
            ParameterCondition = ET.SubElement(ByValueCondition, "ParameterCondition")
            ParameterCondition.set("parameterRef", "")
            ParameterCondition.set("rule", "lessThan")
            ParameterCondition.set("value", "")

        if kwargs["on_sidewalk_test"] == "true":
            Condition = ET.SubElement(ConditionGroup, "Condition")
            Condition.set("name", "criteria_OnSidewalkTest")
            Condition.set("delay", "0")
            Condition.set("conditionEdge", "rising")
            ByValueCondition = ET.SubElement(Condition, "ByValueCondition")
            ParameterCondition = ET.SubElement(ByValueCondition, "ParameterCondition")
            ParameterCondition.set("parameterRef", "")
            ParameterCondition.set("rule", "lessThan")
            ParameterCondition.set("value", "")

        if kwargs["wrong_lane_test"] == "true":
            Condition = ET.SubElement(ConditionGroup, "Condition")
            Condition.set("name", "criteria_WrongLaneTest")
            Condition.set("delay", "0")
            Condition.set("conditionEdge", "rising")
            ByValueCondition = ET.SubElement(Condition, "ByValueCondition")
            ParameterCondition = ET.SubElement(ByValueCondition, "ParameterCondition")
            ParameterCondition.set("parameterRef", "")
            ParameterCondition.set("rule", "lessThan")
            ParameterCondition.set("value", "")

        if kwargs["running_red_light_test"] == "true":
            Condition = ET.SubElement(ConditionGroup, "Condition")
            Condition.set("name", "criteria_RunningRedLightTest")
            Condition.set("delay", "0")
            Condition.set("conditionEdge", "rising")
            ByValueCondition = ET.SubElement(Condition, "ByValueCondition")
            ParameterCondition = ET.SubElement(ByValueCondition, "ParameterCondition")
            ParameterCondition.set("parameterRef", "")
            ParameterCondition.set("rule", "lessThan")
            ParameterCondition.set("value", "")

        if kwargs["running_stop_test"] == "true":
            Condition = ET.SubElement(ConditionGroup, "Condition")
            Condition.set("name", "criteria_RunningStopTest")
            Condition.set("delay", "0")
            Condition.set("conditionEdge", "rising")
            ByValueCondition = ET.SubElement(Condition, "ByValueCondition")
            ParameterCondition = ET.SubElement(ByValueCondition, "ParameterCondition")
            ParameterCondition.set("parameterRef", "")
            ParameterCondition.set("rule", "lessThan")
            ParameterCondition.set("value", "")
        return
