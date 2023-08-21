#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: renpf
# datetime: 20220818

import xml.etree.ElementTree as ET
from .positiongenerator import PositionGenerator
from .utils import *


class ConditionGenerator:
    """
    class of generating Condition.
    """

    def __init__(self, upper_object):
        """
        :param upper_object: string. upper node of ByEntityCondition or ByValueCondition.
        """
        self.upper_object = upper_object

    @catch_exception
    def generate_condition(self, **kwargs):
        """
        :param kwargs: dict. condition params.
        :return: updating of the xsoc file.
        """
        if kwargs["type"] == "distancecondition":
            self.generate_DistanceCondition(**kwargs)
        elif kwargs["type"] == "relativedistancecondition":
            self.generate_RelativeDistanceCondition(**kwargs)
        elif kwargs["type"] == "traveleddistancecondition":
            self.generate_TraveledDistanceCondition(**kwargs)
        elif kwargs["type"] == "accelerationcondition":
            self.generate_AccelerationCondition(**kwargs)
        elif kwargs["type"] == "collisioncondition":
            self.generate_CollisionCondition(**kwargs)
        elif kwargs["type"] == "endofroadcondition":
            self.generate_EndOfRoadCondition(**kwargs)
        elif kwargs["type"] == "offroadcondition":
            self.generate_OffroadCondition(**kwargs)
        elif kwargs["type"] == "reachpositioncondition":
            self.generate_ReachPositionCondition(**kwargs)
        elif kwargs["type"] == "relativespeedcondition":
            self.generate_RelativeSpeedCondition(**kwargs)
        elif kwargs["type"] == "speedcondition":
            self.generate_SpeedCondition(**kwargs)
        elif kwargs["type"] == "standstillcondition":
            self.generate_StandStillCondition(**kwargs)
        elif kwargs["type"] == "timeheadwaycondition":
            self.generate_TimeHeadwayCondition(**kwargs)
        elif kwargs["type"] == "timetocollisioncondition":
            self.generate_TimeToCollisionCondition(**kwargs)
        elif kwargs["type"] == "simulationtimecondition":
            self.generate_SimulationTimeCondition(**kwargs)
        elif kwargs["type"] == "storyboardelementstatecondition":
            self.generate_StoryboardElementStateCondition(**kwargs)
        elif kwargs["type"] == "timeofdaycondition":
            self.generate_TimeOfDayCondition(**kwargs)
        elif kwargs["type"] == "parametercondition":
            self.generate_ParameterCondition(**kwargs)
        elif kwargs["type"] == "trafficsignalcondition":
            self.generate_TrafficSignalCondition(**kwargs)
        else:
            raise TypeError("!" * 10 + "wrong condition type input" + "!" * 10)
        return

    # entity condition
    def generate_DistanceCondition(self, **kwargs):
        """
        :param kwargs: dict. DistanceCondition params.
        :return: updating of the xsoc file.
        """
        ByEntityCondition = ET.SubElement(self.upper_object, "ByEntityCondition")
        TriggeringEntities = ET.SubElement(ByEntityCondition, "TriggeringEntities")
        TriggeringEntities.set("triggeringEntitiesRule", kwargs["params"]["triggeringentities"]["rule"])
        for erf in kwargs["params"]["triggeringentities"]["entityreflist"]:
            EntityRef = ET.SubElement(TriggeringEntities, "EntityRef")
            EntityRef.set("entityRef", erf["entityref"])
        EntityCondition = ET.SubElement(ByEntityCondition, "EntityCondition")
        DistanceCondition = ET.SubElement(EntityCondition, "DistanceCondition")
        DistanceCondition.set("value", kwargs["params"]["value"])
        DistanceCondition.set("freespace", kwargs["params"]["freespace"])
        DistanceCondition.set("alongRoute", kwargs["params"]["alongroute"])
        DistanceCondition.set("rule", kwargs["params"]["rule"])
        Position = ET.SubElement(DistanceCondition, "Position")
        pg = PositionGenerator()
        pg.generate_position(Position, **kwargs)
        return

    def generate_RelativeDistanceCondition(self, **kwargs):
        """
        :param kwargs: dict. RelativeDistanceCondition params.
        :return: updating of the xsoc file.
        """
        ByEntityCondition = ET.SubElement(self.upper_object, "ByEntityCondition")
        TriggeringEntities = ET.SubElement(ByEntityCondition, "TriggeringEntities")
        TriggeringEntities.set("triggeringEntitiesRule", kwargs["params"]["triggeringentities"]["rule"])
        for erf in kwargs["params"]["triggeringentities"]["entityreflist"]:
            EntityRef = ET.SubElement(TriggeringEntities, "EntityRef")
            EntityRef.set("entityRef", erf["entityref"])
        EntityCondition = ET.SubElement(ByEntityCondition, "EntityCondition")
        RelativeDistanceCondition = ET.SubElement(EntityCondition, "RelativeDistanceCondition")
        RelativeDistanceCondition.set("entityRef", kwargs["params"]["entityref"])
        RelativeDistanceCondition.set("relativeDistanceType", kwargs["params"]["relativedistancetype"])
        RelativeDistanceCondition.set("value", kwargs["params"]["value"])
        RelativeDistanceCondition.set("freespace", kwargs["params"]["freespace"])
        RelativeDistanceCondition.set("rule", kwargs["params"]["rule"])
        return

    def generate_TraveledDistanceCondition(self, **kwargs):
        """
        :param kwargs: dict. TraveledDistanceCondition params.
        :return: updating of the xsoc file.
        """
        ByEntityCondition = ET.SubElement(self.upper_object, "ByEntityCondition")
        TriggeringEntities = ET.SubElement(ByEntityCondition, "TriggeringEntities")
        TriggeringEntities.set("triggeringEntitiesRule", kwargs["params"]["triggeringentities"]["rule"])
        for erf in kwargs["params"]["triggeringentities"]["entityreflist"]:
            EntityRef = ET.SubElement(TriggeringEntities, "EntityRef")
            EntityRef.set("entityRef", erf["entityref"])
        EntityCondition = ET.SubElement(ByEntityCondition, "EntityCondition")
        TraveledDistanceCondition = ET.SubElement(EntityCondition, "TraveledDistanceCondition")
        TraveledDistanceCondition.set("value", kwargs["params"]["value"])
        return

    def generate_AccelerationCondition(self, **kwargs):
        """
        :param kwargs: dict. AccelerationCondition params.
        :return: updating of the xsoc file.
        """
        ByEntityCondition = ET.SubElement(self.upper_object, "ByEntityCondition")
        TriggeringEntities = ET.SubElement(ByEntityCondition, "TriggeringEntities")
        TriggeringEntities.set("triggeringEntitiesRule", kwargs["params"]["triggeringentities"]["rule"])
        for erf in kwargs["params"]["triggeringentities"]["entityreflist"]:
            EntityRef = ET.SubElement(TriggeringEntities, "EntityRef")
            EntityRef.set("entityRef", erf["entityref"])
        EntityCondition = ET.SubElement(ByEntityCondition, "EntityCondition")
        AccelerationCondition = ET.SubElement(EntityCondition, "AccelerationCondition")
        AccelerationCondition.set("value", kwargs["params"]["value"])
        AccelerationCondition.set("rule", kwargs["params"]["rule"])
        return

    def generate_CollisionCondition(self, **kwargs):
        """
        :param kwargs: dict. CollisionCondition params.
        :return: updating of the xsoc file.
        """
        ByEntityCondition = ET.SubElement(self.upper_object, "ByEntityCondition")
        TriggeringEntities = ET.SubElement(ByEntityCondition, "TriggeringEntities")
        TriggeringEntities.set("triggeringEntitiesRule", kwargs["params"]["triggeringentities"]["rule"])
        for erf in kwargs["params"]["triggeringentities"]["entityreflist"]:
            EntityRef = ET.SubElement(TriggeringEntities, "EntityRef")
            EntityRef.set("entityRef", erf["entityref"])
        EntityCondition = ET.SubElement(ByEntityCondition, "EntityCondition")
        CollisionCondition = ET.SubElement(EntityCondition, "CollisionCondition")
        if kwargs["params"]["entitychoice"] == "entity":
            EntityRef = ET.SubElement(CollisionCondition, "EntityRef")
            EntityRef.set("entityRef", kwargs["params"]["entityref"])
        if kwargs["params"]["entitychoice"] == "type":
            ByType = ET.SubElement(CollisionCondition, "ByType")
            ByType.set("type", kwargs["params"]["bytype"])
        return

    def generate_EndOfRoadCondition(self, **kwargs):
        """
        :param kwargs: dict. EndOfRoadCondition params.
        :return: updating of the xsoc file.
        """
        ByEntityCondition = ET.SubElement(self.upper_object, "ByEntityCondition")
        TriggeringEntities = ET.SubElement(ByEntityCondition, "TriggeringEntities")
        TriggeringEntities.set("triggeringEntitiesRule", kwargs["params"]["triggeringentities"]["rule"])
        for erf in kwargs["params"]["triggeringentities"]["entityreflist"]:
            EntityRef = ET.SubElement(TriggeringEntities, "EntityRef")
            EntityRef.set("entityRef", erf["entityref"])
        EntityCondition = ET.SubElement(ByEntityCondition, "EntityCondition")
        EndOfRoadCondition = ET.SubElement(EntityCondition, "EndOfRoadCondition")
        EndOfRoadCondition.set("duration", kwargs["params"]["duration"])
        return

    def generate_OffroadCondition(self, **kwargs):
        """
        :param kwargs: dict. OffroadCondition params.
        :return: updating of the xsoc file.
        """
        ByEntityCondition = ET.SubElement(self.upper_object, "ByEntityCondition")
        TriggeringEntities = ET.SubElement(ByEntityCondition, "TriggeringEntities")
        TriggeringEntities.set("triggeringEntitiesRule", kwargs["params"]["triggeringentities"]["rule"])
        for erf in kwargs["params"]["triggeringentities"]["entityreflist"]:
            EntityRef = ET.SubElement(TriggeringEntities, "EntityRef")
            EntityRef.set("entityRef", erf["entityref"])
        EntityCondition = ET.SubElement(ByEntityCondition, "EntityCondition")
        OffroadCondition = ET.SubElement(EntityCondition, "OffroadCondition")
        OffroadCondition.set("duration", kwargs["params"]["duration"])
        return

    def generate_ReachPositionCondition(self, **kwargs):
        """
        :param kwargs: dict. ReachPositionCondition params.
        :return: updating of the xsoc file.
        """
        ByEntityCondition = ET.SubElement(self.upper_object, "ByEntityCondition")
        TriggeringEntities = ET.SubElement(ByEntityCondition, "TriggeringEntities")
        TriggeringEntities.set("triggeringEntitiesRule", kwargs["params"]["triggeringentities"]["rule"])
        for erf in kwargs["params"]["triggeringentities"]["entityreflist"]:
            EntityRef = ET.SubElement(TriggeringEntities, "EntityRef")
            EntityRef.set("entityRef", erf["entityref"])
        EntityCondition = ET.SubElement(ByEntityCondition, "EntityCondition")
        ReachPositionCondition = ET.SubElement(EntityCondition, "ReachPositionCondition")
        ReachPositionCondition.set("tolerance", kwargs["params"]["tolerance"])
        Position = ET.SubElement(ReachPositionCondition, "Position")
        pg = PositionGenerator()
        pg.generate_position(Position, **kwargs)
        return

    def generate_RelativeSpeedCondition(self, **kwargs):
        """
        :param kwargs: dict. RelativeSpeedCondition params.
        :return: updating of the xsoc file.
        """
        ByEntityCondition = ET.SubElement(self.upper_object, "ByEntityCondition")
        TriggeringEntities = ET.SubElement(ByEntityCondition, "TriggeringEntities")
        TriggeringEntities.set("triggeringEntitiesRule", kwargs["params"]["triggeringentities"]["rule"])
        for erf in kwargs["params"]["triggeringentities"]["entityreflist"]:
            EntityRef = ET.SubElement(TriggeringEntities, "EntityRef")
            EntityRef.set("entityRef", erf["entityref"])
        EntityCondition = ET.SubElement(ByEntityCondition, "EntityCondition")
        RelativeSpeedCondition = ET.SubElement(EntityCondition, "RelativeSpeedCondition")
        RelativeSpeedCondition.set("entityRef", kwargs["params"]["entityref"])
        RelativeSpeedCondition.set("value", kwargs["params"]["value"])
        RelativeSpeedCondition.set("rule", kwargs["params"]["rule"])
        return

    def generate_SpeedCondition(self, **kwargs):
        """
        :param kwargs: dict. SpeedCondition params.
        :return: updating of the xsoc file.
        """
        ByEntityCondition = ET.SubElement(self.upper_object, "ByEntityCondition")
        TriggeringEntities = ET.SubElement(ByEntityCondition, "TriggeringEntities")
        TriggeringEntities.set("triggeringEntitiesRule", kwargs["params"]["triggeringentities"]["rule"])
        for erf in kwargs["params"]["triggeringentities"]["entityreflist"]:
            EntityRef = ET.SubElement(TriggeringEntities, "EntityRef")
            EntityRef.set("entityRef", erf["entityref"])
        EntityCondition = ET.SubElement(ByEntityCondition, "EntityCondition")
        SpeedCondition = ET.SubElement(EntityCondition, "SpeedCondition")
        SpeedCondition.set("value", kwargs["params"]["value"])
        SpeedCondition.set("rule", kwargs["params"]["rule"])
        return

    def generate_StandStillCondition(self, **kwargs):
        """
        :param kwargs: dict. StandStillCondition params.
        :return: updating of the xsoc file.
        """
        ByEntityCondition = ET.SubElement(self.upper_object, "ByEntityCondition")
        TriggeringEntities = ET.SubElement(ByEntityCondition, "TriggeringEntities")
        TriggeringEntities.set("triggeringEntitiesRule", kwargs["params"]["triggeringentities"]["rule"])
        for erf in kwargs["params"]["triggeringentities"]["entityreflist"]:
            EntityRef = ET.SubElement(TriggeringEntities, "EntityRef")
            EntityRef.set("entityRef", erf["entityref"])
        EntityCondition = ET.SubElement(ByEntityCondition, "EntityCondition")
        StandStillCondition = ET.SubElement(EntityCondition, "StandStillCondition")
        StandStillCondition.set("duration", kwargs["params"]["duration"])
        return

    def generate_TimeHeadwayCondition(self, **kwargs):
        """
        :param kwargs: dict. TimeHeadwayCondition params.
        :return: updating of the xsoc file.
        """
        ByEntityCondition = ET.SubElement(self.upper_object, "ByEntityCondition")
        TriggeringEntities = ET.SubElement(ByEntityCondition, "TriggeringEntities")
        TriggeringEntities.set("triggeringEntitiesRule", kwargs["params"]["triggeringentities"]["rule"])
        for erf in kwargs["params"]["triggeringentities"]["entityreflist"]:
            EntityRef = ET.SubElement(TriggeringEntities, "EntityRef")
            EntityRef.set("entityRef", erf["entityref"])
        EntityCondition = ET.SubElement(ByEntityCondition, "EntityCondition")
        TimeHeadwayCondition = ET.SubElement(EntityCondition, "TimeHeadwayCondition")
        TimeHeadwayCondition.set("entityRef", kwargs["params"]["entityref"])
        TimeHeadwayCondition.set("value", kwargs["params"]["value"])
        TimeHeadwayCondition.set("freespace", kwargs["params"]["freespace"])
        TimeHeadwayCondition.set("alongRoute", kwargs["params"]["alongroute"])
        TimeHeadwayCondition.set("rule", kwargs["params"]["rule"])
        return

    def generate_TimeToCollisionCondition(self, **kwargs):
        """
        :param kwargs: dict. TimeToCollisionCondition params.
        :return: updating of the xsoc file.
        """
        ByEntityCondition = ET.SubElement(self.upper_object, "ByEntityCondition")
        TriggeringEntities = ET.SubElement(ByEntityCondition, "TriggeringEntities")
        TriggeringEntities.set("triggeringEntitiesRule", kwargs["params"]["triggeringentities"]["rule"])
        for erf in kwargs["params"]["triggeringentities"]["entityreflist"]:
            EntityRef = ET.SubElement(TriggeringEntities, "EntityRef")
            EntityRef.set("entityRef", erf["entityref"])
        EntityCondition = ET.SubElement(ByEntityCondition, "EntityCondition")
        TimeToCollisionCondition = ET.SubElement(EntityCondition, "TimeToCollisionCondition")
        TimeToCollisionCondition.set("value", kwargs["params"]["value"])
        TimeToCollisionCondition.set("freespace", kwargs["params"]["freespace"])
        TimeToCollisionCondition.set("alongRoute", kwargs["params"]["alongroute"])
        TimeToCollisionCondition.set("rule", kwargs["params"]["rule"])
        TimeToCollisionConditionTarget = ET.SubElement(TimeToCollisionCondition, "TimeToCollisionConditionTarget")
        if kwargs["params"]["conditiontarget"] == "position":
            Position = ET.SubElement(TimeToCollisionConditionTarget, "Position")
            pg = PositionGenerator()
            pg.generate_position(Position, **kwargs)
        if kwargs["params"]["conditiontarget"] == "entity":
            EntityRef = ET.SubElement(TimeToCollisionConditionTarget, "EntityRef")
            EntityRef.set("entityRef", kwargs["params"]["entityref"])
        return

    # value condition
    def generate_SimulationTimeCondition(self, **kwargs):
        """
        :param kwargs: dict. SimulationTimeCondition params.
        :return: updating of the xsoc file.
        """
        ByValueCondition = ET.SubElement(self.upper_object, "ByValueCondition")
        SimulationTimeCondition = ET.SubElement(ByValueCondition, "SimulationTimeCondition")
        SimulationTimeCondition.set("value", kwargs["params"]["value"])
        SimulationTimeCondition.set("rule", kwargs["params"]["rule"])
        return

    def generate_StoryboardElementStateCondition(self, **kwargs):
        """
        :param kwargs: dict. StoryboardElementStateCondition params.
        :return: updating of the xsoc file.
        """
        ByValueCondition = ET.SubElement(self.upper_object, "ByValueCondition")
        StoryboardElementStateCondition = ET.SubElement(ByValueCondition, "StoryboardElementStateCondition")
        StoryboardElementStateCondition.set("storyboardElementRef", kwargs["params"]["storyboardelementref"])
        StoryboardElementStateCondition.set("state", kwargs["params"]["state"])
        StoryboardElementStateCondition.set("storyboardElementType", kwargs["params"]["storyboardelementtype"])
        return

    def generate_TimeOfDayCondition(self, **kwargs):
        """
        :param kwargs: dict. TimeOfDayCondition params.
        :return: updating of the xsoc file.
        """
        ByValueCondition = ET.SubElement(self.upper_object, "ByValueCondition")
        TimeOfDayCondition = ET.SubElement(ByValueCondition, "TimeOfDayCondition")
        time_format = kwargs["params"]["datetime"][:10] + 'T' + kwargs["params"]["datetime"][11:]
        TimeOfDayCondition.set("dateTime", time_format)
        TimeOfDayCondition.set("rule", kwargs["params"]["rule"])
        return

    def generate_ParameterCondition(self, **kwargs):
        """
        :param kwargs: dict. ParameterCondition params.
        :return: updating of the xsoc file.
        """
        ByValueCondition = ET.SubElement(self.upper_object, "ByValueCondition")
        ParameterCondition = ET.SubElement(ByValueCondition, "ParameterCondition")
        ParameterCondition.set("parameterRef", kwargs["params"]["parameterref"])
        ParameterCondition.set("rule", kwargs["params"]["rule"])
        ParameterCondition.set("value", kwargs["params"]["value"])
        return

    def generate_TrafficSignalCondition(self, **kwargs):
        """
        :param kwargs: dict. TrafficSignalCondition params.
        :return: updating of the xsoc file.
        """
        ByValueCondition = ET.SubElement(self.upper_object, "ByValueCondition")
        TrafficSignalCondition = ET.SubElement(ByValueCondition, "TrafficSignalCondition")
        TrafficSignalCondition.set("name", "pos=" + kwargs["params"]["x"] + "," + kwargs["params"]["y"] + "id" +
                                   kwargs["params"]["name"])
        TrafficSignalCondition.set("state", kwargs["params"]["state"])
        return
