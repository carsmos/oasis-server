#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: renpf
# datetime: 20220817

import xml.etree.ElementTree as ET
from .positiongenerator import PositionGenerator
from .utils import *
import copy


class ActionGenerator:
    """
    base class of generating Action, all concrete implementations are done in this class.
    """

    def __init__(self):
        pass

    # global actions
    def generate_EnvironmentAction(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of GlobalAction.
        :param kwargs: dict. environment params.
        :return: updating of the xsoc file.
        """
        precipitation_type = translate_precipitation(kwargs["weather"]["precipitation"])
        sun_azimuth_angle, sun_altitude_angle = translate_sun(kwargs["weather"]["sun_azimuth_angle"],
                                                              kwargs["weather"]["sun_altitude_angle"])
        GlobalAction = ET.SubElement(upper_object, "GlobalAction")
        EnvironmentAction = ET.SubElement(GlobalAction, "EnvironmentAction")
        Environment = ET.SubElement(EnvironmentAction, "Environment")
        Environment.set("name", "Environment1")
        TimeOfDay = ET.SubElement(Environment, "TimeOfDay")
        TimeOfDay.set("animation", "true")
        date_time = generate_datetime(sun_altitude_angle)
        TimeOfDay.set("dateTime", date_time)
        Weather = ET.SubElement(Environment, "Weather")
        # if kwargs["weather"]["sky_visibility"] == "true":
        Weather.set("cloudState", kwargs["weather"]["cloudstate"])
        # else:
            # Weather.set("cloudState", "skyOff")
        Sun = ET.SubElement(Weather, "Sun")
        light_intensity = generate_sun_intensity(date_time, kwargs["weather"]["cloudstate"])
        Sun.set("intensity", light_intensity)
        Sun.set("azimuth", sun_azimuth_angle)
        Sun.set("elevation", sun_altitude_angle)
        Fog = ET.SubElement(Weather, "Fog")
        Fog.set("visualRange", kwargs["weather"]["fog_visualrange"])
        Precipitation = ET.SubElement(Weather, "Precipitation")
        Precipitation.set("precipitationType", precipitation_type)
        Precipitation.set("intensity", kwargs["weather"]["precipitation"])
        RoadCondition = ET.SubElement(Environment, "RoadCondition")
        RoadCondition.set("frictionScaleFactor", "1.0")
        return

    def generate_TrafficSignalStateAction(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of GlobalAction. in Init is Actions, in Story is Action
        :param kwargs: dict. environment params.
        :return: updating of the xsoc file.
        """
        GlobalAction = ET.SubElement(upper_object, "GlobalAction")
        InfrastructureAction = ET.SubElement(GlobalAction, "InfrastructureAction")
        TrafficSignalAction = ET.SubElement(InfrastructureAction, "TrafficSignalAction")
        TrafficSignalStateAction = ET.SubElement(TrafficSignalAction, "TrafficSignalStateAction")
        # TrafficSignalStateAction.set("name", kwargs["params"]["name"])
        TrafficSignalStateAction.set("name", "pos=" + kwargs["params"]["x"] + "," + kwargs["params"]["y"] + "id" +
                                     kwargs["params"]["name"])  # pos=20,100id1234
        TrafficSignalStateAction.set("state", kwargs["params"]["state"])
        return

    # private action
    def generate_SpeedAction(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of PrivateAction.
        :param kwargs: dict. speed params.
        :return: updating of the xsoc file.
        """
        # for init speed action {'type':'absolute','params':{'value':1}}
        # for story speed action {'type':'speedaction','params':{'targetspeed':{'type':'absolute','params':{'value':1}}
        PrivateAction = ET.SubElement(upper_object, "PrivateAction")
        LongitudinalAction = ET.SubElement(PrivateAction, "LongitudinalAction")
        SpeedAction = ET.SubElement(LongitudinalAction, "SpeedAction")
        SpeedActionDynamics = ET.SubElement(SpeedAction, "SpeedActionDynamics")
        SpeedActionTarget = ET.SubElement(SpeedAction, "SpeedActionTarget")
        SpeedActionDynamics.set("dynamicsShape", "step")
        SpeedActionDynamics.set("value", "0")
        SpeedActionDynamics.set("dynamicsDimension", "time")
        if kwargs["type"] in ["absolute", "relative"]:
            if kwargs["type"] == "absolute":
                AbsoluteTargetSpeed = ET.SubElement(SpeedActionTarget, "AbsoluteTargetSpeed")
                AbsoluteTargetSpeed.set("value", kwargs["params"]["value"])
            else:
                RelativeTargetSpeed = ET.SubElement(SpeedActionTarget, "RelativeTargetSpeed")
                RelativeTargetSpeed.set("entityRef", kwargs["params"]["entityref"])
                RelativeTargetSpeed.set("value", kwargs["params"]["value"])
                RelativeTargetSpeed.set("speedTargetValueType", kwargs["params"]["valuetype"])
                RelativeTargetSpeed.set("continuous", kwargs["params"]["continuous"])
        elif kwargs["type"] in ["speedaction"]:
            SpeedActionDynamics.set("dynamicsShape", kwargs["params"]["transitiondynamics"]["dynamicsshape"])
            SpeedActionDynamics.set("value", kwargs["params"]["transitiondynamics"]["value"])
            SpeedActionDynamics.set("dynamicsDimension", kwargs["params"]["transitiondynamics"]["dynamicsdimension"])
            if kwargs["params"]["targetspeed"]["type"] == "absolute":
                AbsoluteTargetSpeed = ET.SubElement(SpeedActionTarget, "AbsoluteTargetSpeed")
                AbsoluteTargetSpeed.set("value", kwargs["params"]["targetspeed"]["params"]["value"])
            else:
                RelativeTargetSpeed = ET.SubElement(SpeedActionTarget, "RelativeTargetSpeed")
                RelativeTargetSpeed.set("entityRef", kwargs["params"]["targetspeed"]["params"]["entityref"])
                RelativeTargetSpeed.set("value", kwargs["params"]["targetspeed"]["params"]["value"])
                RelativeTargetSpeed.set("speedTargetValueType", kwargs["params"]["targetspeed"]["params"]["valuetype"])
                RelativeTargetSpeed.set("continuous", kwargs["params"]["targetspeed"]["params"]["continuous"])
        return

    def generate_LongitudinalDistanceAction(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of PrivateAction.
        :param kwargs: dict. longitudinaldistance params.
        :return: updating of the xsoc file.
        """
        PrivateAction = ET.SubElement(upper_object, "PrivateAction")
        LongitudinalAction = ET.SubElement(PrivateAction, "LongitudinalAction")
        LongitudinalDistanceAction = ET.SubElement(LongitudinalAction, "LongitudinalDistanceAction")
        LongitudinalDistanceAction.set("entityRef", kwargs["params"]["entityref"])
        if kwargs["params"]["distance"] != "false":
            LongitudinalDistanceAction.set("distance", kwargs["params"]["distance"])
        if kwargs["params"]["timegap"] != "false":
            LongitudinalDistanceAction.set("timeGap", kwargs["params"]["timegap"])
        LongitudinalDistanceAction.set("freespace", kwargs["params"]["freespace"])
        LongitudinalDistanceAction.set("continuous", kwargs["params"]["continuous"])
        if len(list(kwargs["params"]["dynamicconstraints"].keys())) > 0:
            DynamicConstraints = ET.SubElement(LongitudinalDistanceAction, "DynamicConstraints")
            DynamicConstraints.set("maxAcceleration", kwargs["params"]["dynamicconstraints"]["maxacceleration"])
            DynamicConstraints.set("maxDeceleration", kwargs["params"]["dynamicconstraints"]["maxdeceleration"])
            DynamicConstraints.set("maxSpeed", kwargs["params"]["dynamicconstraints"]["maxspeed"])
        return

    def generate_LaneChangeAction(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of PrivateAction.
        :param kwargs: dict. changelane params.
        :return: updating of the xsoc file.
        """
        PrivateAction = ET.SubElement(upper_object, "PrivateAction")
        LateralAction = ET.SubElement(PrivateAction, "LateralAction")
        LaneChangeAction = ET.SubElement(LateralAction, "LaneChangeAction")
        LaneChangeAction.set("targetLaneOffset", kwargs["params"]["targetlaneoffset"])
        LaneChangeActionDynamics = ET.SubElement(LaneChangeAction, "LaneChangeActionDynamics")
        LaneChangeActionDynamics.set("dynamicsShape", kwargs["params"]["transitiondynamics"]["dynamicsshape"])
        LaneChangeActionDynamics.set("value", kwargs["params"]["transitiondynamics"]["value"])
        LaneChangeActionDynamics.set("dynamicsDimension", kwargs["params"]["transitiondynamics"]["dynamicsdimension"])
        LaneChangeTarget = ET.SubElement(LaneChangeAction, "LaneChangeTarget")
        if kwargs["params"]["targetlane"]["type"] == "absolute":
            AbsoluteTargetLane = ET.SubElement(LaneChangeTarget, "AbsoluteTargetLane")
            AbsoluteTargetLane.set("value", kwargs["params"]["targetlane"]["params"]["laneid"])
        else:
            RelativeTargetLane = ET.SubElement(LaneChangeTarget, "RelativeTargetLane")
            RelativeTargetLane.set("entityRef", kwargs["params"]["targetlane"]["params"]["entityref"])
            RelativeTargetLane.set("value", kwargs["params"]["targetlane"]["params"]["value"])
        return

    def generate_LaneOffsetAction(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of PrivateAction.
        :param kwargs: dict. laneoffset params.
        :return: updating of the xsoc file.
        """
        PrivateAction = ET.SubElement(upper_object, "PrivateAction")
        LateralAction = ET.SubElement(PrivateAction, "LateralAction")
        LaneOffsetAction = ET.SubElement(LateralAction, "LaneOffsetAction")
        LaneOffsetAction.set("continuous", kwargs["params"]["continuous"])
        LaneOffsetActionDynamics = ET.SubElement(LaneOffsetAction, "LaneOffsetActionDynamics")
        LaneOffsetActionDynamics.set("maxLateralAcc", kwargs["params"]["laneoffsetactiondynamics"]["maxlateralacc"])
        LaneOffsetActionDynamics.set("dynamicsShape", kwargs["params"]["laneoffsetactiondynamics"]["dynamicsshape"])
        LaneOffsetTarget = ET.SubElement(LaneOffsetAction, "LaneOffsetTarget")
        if kwargs["params"]["laneoffsettarget"]["type"] == "absolute":
            AbsoluteTargetLaneOffset = ET.SubElement(LaneOffsetTarget, "AbsoluteTargetLaneOffset")
            AbsoluteTargetLaneOffset.set("value", kwargs["params"]["laneoffsettarget"]["params"]["value"])
        else:
            RelativeTargetLaneOffset = ET.SubElement(LaneOffsetTarget, "RelativeTargetLaneOffset")
            RelativeTargetLaneOffset.set("entityRef", kwargs["params"]["laneoffsettarget"]["params"]["entityref"])
            RelativeTargetLaneOffset.set("value", kwargs["params"]["laneoffsettarget"]["params"]["value"])
        return

    def generate_LateralDistanceAction(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of PrivateAction.
        :param kwargs: dict. lateraldistance params.
        :return: updating of the xsoc file.
        """
        PrivateAction = ET.SubElement(upper_object, "PrivateAction")
        LateralAction = ET.SubElement(PrivateAction, "LateralAction")
        LateralDistanceAction = ET.SubElement(LateralAction, "LateralDistanceAction")
        LateralDistanceAction.set("entityRef", kwargs["params"]["entityref"])
        LateralDistanceAction.set("distance", kwargs["params"]["distance"])
        LateralDistanceAction.set("freespace", kwargs["params"]["freespace"])
        LateralDistanceAction.set("continuous", kwargs["params"]["continuous"])
        if len(list(kwargs["params"]["dynamicconstraints"].keys())) > 0:
            DynamicConstraints = ET.SubElement(LateralDistanceAction, "DynamicConstraints")
            DynamicConstraints.set("maxAcceleration", kwargs["params"]["dynamicconstraints"]["maxacceleration"])
            DynamicConstraints.set("maxDeceleration", kwargs["params"]["dynamicconstraints"]["maxdeceleration"])
            DynamicConstraints.set("maxSpeed", kwargs["params"]["dynamicconstraints"]["maxspeed"])
        return

    def generate_AssignRouteAction(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of PrivateAction.
        :param kwargs: dict. assignroute params.
        :return: updating of the xsoc file.
        """
        PrivateAction = ET.SubElement(upper_object, "PrivateAction")
        RoutingAction = ET.SubElement(PrivateAction, "RoutingAction")
        AssignRouteAction = ET.SubElement(RoutingAction, "AssignRouteAction")
        Route = ET.SubElement(AssignRouteAction, "Route")
        Route.set("closed", kwargs["params"]["closed"])
        Route.set("name", kwargs["params"]["name"])
        Waypoint_list = kwargs["params"]["waypoint"]
        for wp in Waypoint_list:
            Waypoint = ET.SubElement(Route, "Waypoint")
            # Waypoint.set("routeStrategy", wp["routestrategy"])
            Waypoint.set("routeStrategy", "shortest")
            Position = ET.SubElement(Waypoint, "Position")
            pg = PositionGenerator()
            pg.generate_position(Position, **wp)
        return

    def generate_FollowTrajectoryAction(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of PrivateAction.
        :param kwargs: dict. followtrajectory params.
        :return: updating of the xsoc file.
        """
        PrivateAction = ET.SubElement(upper_object, "PrivateAction")
        RoutingAction = ET.SubElement(PrivateAction, "RoutingAction")
        FollowTrajectoryAction = ET.SubElement(RoutingAction, "FollowTrajectoryAction")
        Trajectory = ET.SubElement(FollowTrajectoryAction, "Trajectory")
        Trajectory.set("closed", kwargs["params"]["closed"])
        Trajectory.set("name", kwargs["params"]["name"])
        Shape = ET.SubElement(Trajectory, "Shape")
        Polyline = ET.SubElement(Shape, "Polyline")
        Vertex_list = kwargs["params"]["shape"]
        for vt in Vertex_list:
            Vertex = ET.SubElement(Polyline, "Vertex")
            # if kwargs["params"]["timerederence"]["type"] == "timing":
            Vertex.set("time", vt["time"])
            Position = ET.SubElement(Vertex, "Position")
            pg = PositionGenerator()
            pg.generate_position(Position, **vt)
        TimeReference = ET.SubElement(FollowTrajectoryAction, "TimeReference")
        if kwargs["params"]["timerederence"]["type"] == "none":  # none
            Nonee = ET.SubElement(TimeReference, "None")
            pass
        else:  # timing
            Timing = ET.SubElement(TimeReference, "Timing")
            Timing.set("domainAbsoluteRelative", kwargs["params"]["timerederence"]["params"]["domainabsoluterelative"])
            Timing.set("offset", kwargs["params"]["timerederence"]["params"]["offset"])
            Timing.set("scale", kwargs["params"]["timerederence"]["params"]["scale"])
        TrajectoryFollowingMode = ET.SubElement(FollowTrajectoryAction, "TrajectoryFollowingMode")
        TrajectoryFollowingMode.set("followingMode", "follow")
        return

    def generate_AcquirePositionAction(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of PrivateAction.
        :param kwargs: dict. acquireposition params.
        :return: updating of the xsoc file.
        """
        # {'type':'acquirepositionaction','params':{'position':{'type':'worldposition','params':{}}}}
        PrivateAction = ET.SubElement(upper_object, "PrivateAction")
        RoutingAction = ET.SubElement(PrivateAction, "RoutingAction")
        AcquirePositionAction = ET.SubElement(RoutingAction, "AcquirePositionAction")
        Position = ET.SubElement(AcquirePositionAction, "Position")
        pg = PositionGenerator()
        pg.generate_position(Position, **kwargs)
        return

    def generate_SynchronizeAction(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of PrivateAction.
        :param kwargs: dict. synchronize params.
        :return: updating of the xsoc file.
        """
        PrivateAction = ET.SubElement(upper_object, "PrivateAction")
        SynchronizeAction = ET.SubElement(PrivateAction, "SynchronizeAction")
        SynchronizeAction.set("masterEntityRef", kwargs["params"]["masterentityref"])
        TargetPositionMaster = ET.SubElement(SynchronizeAction, "TargetPositionMaster")
        targetpositionmaster_kwargs = copy.deepcopy(kwargs)
        targetpositionmaster_kwargs["params"].pop("targetposition")
        pg = PositionGenerator()
        pg.generate_position(TargetPositionMaster, **targetpositionmaster_kwargs)
        TargetPosition = ET.SubElement(SynchronizeAction, "TargetPosition")
        targetposition_kwargs = copy.deepcopy(kwargs)
        targetposition_kwargs["params"].pop("targetpositionmaster")
        pg = PositionGenerator()
        pg.generate_position(TargetPosition, **targetposition_kwargs)
        FinalSpeed = ET.SubElement(SynchronizeAction, "FinalSpeed")
        if kwargs["params"]["finalspeed"]["type"] == "absolutespeed":
            AbsoluteSpeed = ET.SubElement(FinalSpeed, "AbsoluteSpeed")
            AbsoluteSpeed.set("value", kwargs["params"]["finalspeed"]["params"]["value"])
        else:
            RelativeSpeedToMaster = ET.SubElement(FinalSpeed, "RelativeSpeedToMaster")
            RelativeSpeedToMaster.set("value", kwargs["params"]["finalspeed"]["params"]["value"])
            RelativeSpeedToMaster.set("speedTargetValueType",
                                      kwargs["params"]["finalspeed"]["params"]["speedtargetvaluetype"])
        return

    def generate_TeleportAction(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of PrivateAction.
        :param kwargs: dict. teleport params.
        :return: updating of the xsoc file.
        """
        PrivateAction = ET.SubElement(upper_object, "PrivateAction")
        TeleportAction = ET.SubElement(PrivateAction, "TeleportAction")
        Position = ET.SubElement(TeleportAction, "Position")
        pg = PositionGenerator()
        pg.generate_position(Position, **kwargs)
        return


class InitActionGenerator(ActionGenerator):
    """
    inherited class of ActionGenerator, for generating Action in Init.
    """

    def __init__(self, upper_object):
        """
        :param upper_object: string. upper node of Action, is Init-Actions.
        """
        super(InitActionGenerator, self).__init__()
        self.upper_object = upper_object

    @catch_exception
    def generate_global_action(self, **kwargs):
        """
        :param kwargs: dict. environment params.
        :return: updating of the xsoc file.
        """
        self.generate_EnvironmentAction(self.upper_object, **kwargs)
        return

    @catch_exception
    def generate_private_action(self, **kwargs):
        """
        :param kwargs: dict. private_action params.
        :return: updating of the xsoc file.
        """
        Private = ET.SubElement(self.upper_object, "Private")
        Private.set("entityRef", kwargs["name"])
        self.generate_SpeedAction(Private, **kwargs["speed"])
        self.generate_TeleportAction(Private, **kwargs)
        return


class StoryActionGenerator(ActionGenerator):
    """
    inherited class of ActionGenerator, for generating Action in Story.
    """

    def __init__(self, upper_object):
        """
        :param upper_object: string. upper node of Action, is Event-Action.
        """
        super(StoryActionGenerator, self).__init__()
        self.upper_object = upper_object

    @catch_exception
    def generate_private_action(self, **kwargs):
        """
        :param kwargs: dict. private_action params.
        :return: updating of the xsoc file.
        """
        if kwargs["type"] == "speedaction":
            self.generate_SpeedAction(self.upper_object, **kwargs)
        elif kwargs["type"] == "longitudinaldistanceaction":
            self.generate_LongitudinalDistanceAction(self.upper_object, **kwargs)
        elif kwargs["type"] == "lanechangeaction":
            self.generate_LaneChangeAction(self.upper_object, **kwargs)
        elif kwargs["type"] == "laneoffsetaction":
            self.generate_LaneOffsetAction(self.upper_object, **kwargs)
        elif kwargs["type"] == "lateraldistanceaction":
            self.generate_LateralDistanceAction(self.upper_object, **kwargs)
        elif kwargs["type"] == "assignrouteaction":
            self.generate_AssignRouteAction(self.upper_object, **kwargs)
        elif kwargs["type"] == "followtrajectoryaction":
            self.generate_FollowTrajectoryAction(self.upper_object, **kwargs)
        elif kwargs["type"] == "acquirepositionaction":
            self.generate_AcquirePositionAction(self.upper_object, **kwargs)
        elif kwargs["type"] == "synchronizeaction":
            self.generate_SynchronizeAction(self.upper_object, **kwargs)
        elif kwargs["type"] == "teleportaction":
            self.generate_TeleportAction(self.upper_object, **kwargs)
        elif kwargs["type"] == "trafficsignalstateaction":
            self.generate_TrafficSignalStateAction(self.upper_object, **kwargs)
        else:
            raise TypeError("only SpeedAction TeleportAction LaneChangeAction supported.")
        return
