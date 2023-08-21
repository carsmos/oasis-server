#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: renpf
# datetime: 20220818
import xml.etree.ElementTree as ET
from .utils import *


class PositionGenerator:
    """
    class of generating Position, all concrete implementations are done in this class.
    """

    def __init__(self):
        pass

    # @catch_exception
    def generate_position(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of Position.
        :param kwargs: dict. params of Position.
        :return: updating of the xsoc file.
        """
        if "start_position" in list(kwargs.keys()):
            if kwargs["start_position"]["type"] == "worldposition":
                self.generate_WorldPosition(upper_object, **(kwargs["start_position"]))
            elif kwargs["start_position"]["type"] == "roadposition":
                self.generate_RoadPosition(upper_object, **(kwargs["start_position"]))
            elif kwargs["start_position"]["type"] == "laneposition":
                self.generate_LanePosition(upper_object, **(kwargs["start_position"]))
            elif kwargs["start_position"]["type"] == "relativeworldposition":
                self.generate_RelativeWorldPosition(upper_object, **(kwargs["start_position"]))
            elif kwargs["start_position"]["type"] == "relativeobjectposition":
                self.generate_RelativeObjectPosition(upper_object, **(kwargs["start_position"]))
            elif kwargs["start_position"]["type"] == "relativeroadposition":
                self.generate_RelativeRoadPosition(upper_object, **(kwargs["start_position"]))
            elif kwargs["start_position"]["type"] == "relativelaneposition":
                self.generate_RelativeLanePosition(upper_object, **(kwargs["start_position"]))
            else:
                raise TypeError("The type passed in is not supported")
        elif "position" in list(kwargs["params"].keys()):
            if len(list(kwargs["params"]["position"])) > 0:
                if kwargs["params"]["position"]["type"] == "worldposition":
                    self.generate_WorldPosition(upper_object, **(kwargs["params"]["position"]))
                elif kwargs["params"]["position"]["type"] == "roadposition":
                    self.generate_RoadPosition(upper_object, **(kwargs["params"]["position"]))
                elif kwargs["params"]["position"]["type"] == "laneposition":
                    self.generate_LanePosition(upper_object, **(kwargs["params"]["position"]))
                elif kwargs["params"]["position"]["type"] == "relativeworldposition":
                    self.generate_RelativeWorldPosition(upper_object, **(kwargs["params"]["position"]))
                elif kwargs["params"]["position"]["type"] == "relativeobjectposition":
                    self.generate_RelativeObjectPosition(upper_object, **(kwargs["params"]["position"]))
                elif kwargs["params"]["position"]["type"] == "relativeroadposition":
                    self.generate_RelativeRoadPosition(upper_object, **(kwargs["params"]["position"]))
                elif kwargs["params"]["position"]["type"] == "relativelaneposition":
                    self.generate_RelativeLanePosition(upper_object, **(kwargs["params"]["position"]))
                else:
                    raise TypeError("The entered location type is not supported")
            else:
                if "targetpositionmaster" in list(kwargs["params"].keys()):
                    if kwargs["params"]["targetpositionmaster"]["type"] == "worldposition":
                        self.generate_WorldPosition(upper_object, **(kwargs["params"]["targetpositionmaster"]))
                    elif kwargs["params"]["targetpositionmaster"]["type"] == "roadposition":
                        self.generate_RoadPosition(upper_object, **(kwargs["params"]["targetpositionmaster"]))
                    elif kwargs["params"]["targetpositionmaster"]["type"] == "laneposition":
                        self.generate_LanePosition(upper_object, **(kwargs["params"]["targetpositionmaster"]))
                    elif kwargs["params"]["targetpositionmaster"]["type"] == "relativeworldposition":
                        self.generate_RelativeWorldPosition(upper_object, **(kwargs["params"]["targetpositionmaster"]))
                    elif kwargs["params"]["targetpositionmaster"]["type"] == "relativeobjectposition":
                        self.generate_RelativeObjectPosition(upper_object, **(kwargs["params"]["targetpositionmaster"]))
                    elif kwargs["params"]["targetpositionmaster"]["type"] == "relativeroadposition":
                        self.generate_RelativeRoadPosition(upper_object, **(kwargs["params"]["targetpositionmaster"]))
                    elif kwargs["params"]["targetpositionmaster"]["type"] == "relativelaneposition":
                        self.generate_RelativeLanePosition(upper_object, **(kwargs["params"]["targetpositionmaster"]))
                    else:
                        raise TypeError("The entered location type is not supported")
                elif "targetposition" in list(kwargs["params"].keys()):
                    if kwargs["params"]["targetposition"]["type"] == "worldposition":
                        self.generate_WorldPosition(upper_object, **(kwargs["params"]["targetposition"]))
                    elif kwargs["params"]["targetposition"]["type"] == "roadposition":
                        self.generate_RoadPosition(upper_object, **(kwargs["params"]["targetposition"]))
                    elif kwargs["params"]["targetposition"]["type"] == "laneposition":
                        self.generate_LanePosition(upper_object, **(kwargs["params"]["targetposition"]))
                    elif kwargs["params"]["targetposition"]["type"] == "relativeworldposition":
                        self.generate_RelativeWorldPosition(upper_object, **(kwargs["params"]["targetposition"]))
                    elif kwargs["params"]["targetposition"]["type"] == "relativeobjectposition":
                        self.generate_RelativeObjectPosition(upper_object, **(kwargs["params"]["targetposition"]))
                    elif kwargs["params"]["targetposition"]["type"] == "relativeroadposition":
                        self.generate_RelativeRoadPosition(upper_object, **(kwargs["params"]["targetposition"]))
                    elif kwargs["params"]["targetposition"]["type"] == "relativelaneposition":
                        self.generate_RelativeLanePosition(upper_object, **(kwargs["params"]["targetposition"]))
                    else:
                        raise TypeError("The entered location type is not supported")
                else:
                    raise TypeError("wrong format of kwargs")
        else:
            raise TypeError("wrong format of kwargs")
        return

    def generate_WorldPosition(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of WorldPosition, is Position.
        :param kwargs: dict. params of WorldPosition.
        :return: updating of the xsoc file.
        """
        WorldPosition = ET.SubElement(upper_object, "WorldPosition")
        WorldPosition.set("x", kwargs["params"]["x"])
        WorldPosition.set("y", kwargs["params"]["y"])
        WorldPosition.set("z", kwargs["params"]["z"])
        WorldPosition.set("h", translate_hpr(kwargs["params"]["h"]))
        WorldPosition.set("p", translate_hpr(kwargs["params"]["p"]))
        WorldPosition.set("r", translate_hpr(kwargs["params"]["r"]))
        return

    def generate_RoadPosition(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of RoadPosition, is Position.
        :param kwargs: dict. params of RoadPosition.
        :return: updating of the xsoc file.
        """
        RoadPosition = ET.SubElement(upper_object, "RoadPosition")
        RoadPosition.set("roadId", kwargs["params"]["roadid"])
        RoadPosition.set("s", kwargs["params"]["s"])
        RoadPosition.set("t", kwargs["params"]["t"])
        Orientation = ET.SubElement(RoadPosition, "Orientation")
        Orientation.set("h", translate_hpr(kwargs["params"]["orientation"]["h"]))
        Orientation.set("p", translate_hpr(kwargs["params"]["orientation"]["p"]))
        Orientation.set("r", translate_hpr(kwargs["params"]["orientation"]["r"]))
        Orientation.set("type", kwargs["params"]["orientation"]["reftype"])
        return

    def generate_LanePosition(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of LanePosition, is Position.
        :param kwargs: dict. params of LanePosition.
        :return: updating of the xsoc file.
        """
        LanePosition = ET.SubElement(upper_object, "LanePosition")
        LanePosition.set("roadId", kwargs["params"]["roadid"])
        LanePosition.set("laneId", kwargs["params"]["laneid"])
        LanePosition.set("offset", kwargs["params"]["offset"])
        LanePosition.set("s", kwargs["params"]["s"])
        Orientation = ET.SubElement(LanePosition, "Orientation")
        Orientation.set("h", translate_hpr(kwargs["params"]["orientation"]["h"]))
        Orientation.set("p", translate_hpr(kwargs["params"]["orientation"]["p"]))
        Orientation.set("r", translate_hpr(kwargs["params"]["orientation"]["r"]))
        Orientation.set("type", kwargs["params"]["orientation"]["reftype"])
        return

    def generate_RelativeWorldPosition(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of RelativeWorldPosition, is Position.
        :param kwargs: dict. params of RelativeWorldPosition.
        :return: updating of the xsoc file.
        """
        RelativeWorldPosition = ET.SubElement(upper_object, "RelativeWorldPosition")
        RelativeWorldPosition.set("entityRef", kwargs["params"]["entityref"])
        RelativeWorldPosition.set("dx", kwargs["params"]["dx"])
        RelativeWorldPosition.set("dy", kwargs["params"]["dy"])
        RelativeWorldPosition.set("dz", kwargs["params"]["dz"])
        Orientation = ET.SubElement(RelativeWorldPosition, "Orientation")
        Orientation.set("h", translate_hpr(kwargs["params"]["orientation"]["h"]))
        Orientation.set("p", translate_hpr(kwargs["params"]["orientation"]["p"]))
        Orientation.set("r", translate_hpr(kwargs["params"]["orientation"]["r"]))
        Orientation.set("type", kwargs["params"]["orientation"]["reftype"])
        return

    def generate_RelativeObjectPosition(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of RelativeObjectPosition, is Position.
        :param kwargs: dict. params of RelativeObjectPosition.
        :return: updating of the xsoc file.
        """
        RelativeObjectPosition = ET.SubElement(upper_object, "RelativeObjectPosition")
        RelativeObjectPosition.set("entityRef", kwargs["params"]["entityref"])
        RelativeObjectPosition.set("dx", kwargs["params"]["dx"])
        RelativeObjectPosition.set("dy", kwargs["params"]["dy"])
        RelativeObjectPosition.set("dz", kwargs["params"]["dz"])
        Orientation = ET.SubElement(RelativeObjectPosition, "Orientation")
        Orientation.set("h", translate_hpr(kwargs["params"]["orientation"]["h"]))
        Orientation.set("p", translate_hpr(kwargs["params"]["orientation"]["p"]))
        Orientation.set("r", translate_hpr(kwargs["params"]["orientation"]["r"]))
        Orientation.set("type", kwargs["params"]["orientation"]["reftype"])
        return

    def generate_RelativeRoadPosition(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of RelativeRoadPosition, is Position.
        :param kwargs: dict. params of RelativeRoadPosition.
        :return: updating of the xsoc file.
        """
        RelativeRoadPosition = ET.SubElement(upper_object, "RelativeRoadPosition")
        RelativeRoadPosition.set("entityRef", kwargs["params"]["entityref"])
        RelativeRoadPosition.set("ds", kwargs["params"]["ds"])
        RelativeRoadPosition.set("dt", kwargs["params"]["dt"])
        Orientation = ET.SubElement(RelativeRoadPosition, "Orientation")
        Orientation.set("h", translate_hpr(kwargs["params"]["orientation"]["h"]))
        Orientation.set("p", translate_hpr(kwargs["params"]["orientation"]["p"]))
        Orientation.set("r", translate_hpr(kwargs["params"]["orientation"]["r"]))
        Orientation.set("type", kwargs["params"]["orientation"]["reftype"])
        return

    def generate_RelativeLanePosition(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of RelativeLanePosition, is Position.
        :param kwargs: dict. params of RelativeLanePosition.
        :return: updating of the xsoc file.
        """
        RelativeLanePosition = ET.SubElement(upper_object, "RelativeLanePosition")
        RelativeLanePosition.set("entityRef", kwargs["params"]["entityref"])
        RelativeLanePosition.set("offset", kwargs["params"]["offset"])
        RelativeLanePosition.set("ds", kwargs["params"]["ds"])
        RelativeLanePosition.set("dLane", kwargs["params"]["dlane"])
        Orientation = ET.SubElement(RelativeLanePosition, "Orientation")
        Orientation.set("h", translate_hpr(kwargs["params"]["orientation"]["h"]))
        Orientation.set("p", translate_hpr(kwargs["params"]["orientation"]["p"]))
        Orientation.set("r", translate_hpr(kwargs["params"]["orientation"]["r"]))
        Orientation.set("type", kwargs["params"]["orientation"]["reftype"])
        return
