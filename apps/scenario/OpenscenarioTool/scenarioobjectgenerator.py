#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: renpf
# datetime: 20220817
import xml.etree.ElementTree as ET
from .utils import *


class ScenarioObjectGenerator:
    """
    generate one ScenarioObject of the Entites
    """

    def __init__(self, catalog_file_path):
        """
        :param catalog_file_path: string. location of the catalog json file.
        """
        self.npc_list = []
        tree = ET.parse(catalog_file_path)
        root = tree.getroot()
        for layer_1 in root:  # {'name': 'VehicleCatalog'}
            for layer_2 in layer_1:  # tag:Vehicle. attrib:{'name': 'vehicle.tesla.model3', 'vehicleCategory': 'car'}
                vehicle_dict = {}
                vehicle_dict[layer_2.tag] = layer_2.attrib
                for layer_3 in layer_2:
                    vehicle_dict[layer_3.tag] = layer_3.attrib
                    for layer_4 in layer_3:
                        vehicle_dict[layer_4.tag] = layer_4.attrib
                self.npc_list.append(vehicle_dict)

    def generate_scenarioobject(self, upper_object, **kwargs):
        """
        :param upper_object: string. upper node of ScenarioObject, is Entites.
        :param kwargs: dict. params of ScenarioObject.
        :return: updating of the xsoc file.
        """
        ScenarioObject = ET.SubElement(upper_object, "ScenarioObject")
        ScenarioObject.set("name", kwargs["name"])
        for npc in self.npc_list:
            if "Vehicle" in list(npc.keys()):
                if kwargs.get("model") == npc["Vehicle"]["name"]:
                    Vehicle = ET.SubElement(ScenarioObject, "Vehicle")
                    Vehicle.set("name", npc["Vehicle"]["name"])
                    Vehicle.set("vehicleCategory", npc["Vehicle"]["vehicleCategory"])
                    BoundingBox = ET.SubElement(Vehicle, "BoundingBox")
                    Center = ET.SubElement(BoundingBox, "Center")
                    Center.set("x", npc["Center"]["x"])
                    Center.set("y", npc["Center"]["y"])
                    Center.set("z", npc["Center"]["z"])
                    Dimensions = ET.SubElement(BoundingBox, "Dimensions")
                    Dimensions.set("width", npc["Dimensions"]["width"])
                    Dimensions.set("length", npc["Dimensions"]["length"])
                    Dimensions.set("height", npc["Dimensions"]["height"])
                    Performance = ET.SubElement(Vehicle, "Performance")
                    Performance.set("maxSpeed", npc["Performance"]["maxSpeed"])
                    Performance.set("maxAcceleration", npc["Performance"]["maxAcceleration"])
                    Performance.set("maxDeceleration", npc["Performance"]["maxDeceleration"])
                    Axles = ET.SubElement(Vehicle, "Axles")
                    FrontAxle = ET.SubElement(Axles, "FrontAxle")
                    FrontAxle.set("maxSteering", npc["FrontAxle"]["maxSteering"])
                    FrontAxle.set("wheelDiameter", npc["FrontAxle"]["wheelDiameter"])
                    FrontAxle.set("trackWidth", npc["FrontAxle"]["trackWidth"])
                    FrontAxle.set("positionX", npc["FrontAxle"]["positionX"])
                    FrontAxle.set("positionZ", npc["FrontAxle"]["positionZ"])
                    RearAxle = ET.SubElement(Axles, "RearAxle")
                    RearAxle.set("maxSteering", npc["FrontAxle"]["maxSteering"])
                    RearAxle.set("wheelDiameter", npc["FrontAxle"]["wheelDiameter"])
                    RearAxle.set("trackWidth", npc["FrontAxle"]["trackWidth"])
                    RearAxle.set("positionX", npc["FrontAxle"]["positionX"])
                    RearAxle.set("positionZ", npc["FrontAxle"]["positionZ"])
                    Properties = ET.SubElement(Vehicle, "Properties")
                    Property = ET.SubElement(Properties, "Property")
                    if kwargs["name"] == "ego_vehicle":
                        Property.set("name", "type")
                        Property.set("value", "ego_vehicle")
                    else:
                        Property.set("name", "type")
                        Property.set("value", "simulation")
            if "Pedestrian" in list(npc.keys()):
                if kwargs.get("model") == npc["Pedestrian"]["name"]:
                    Pedestrian = ET.SubElement(ScenarioObject, "Pedestrian")
                    Pedestrian.set("name", npc["Pedestrian"]["name"])
                    Pedestrian.set("model", npc["Pedestrian"]["name"])
                    Pedestrian.set("mass", "65")
                    Pedestrian.set("pedestrianCategory", npc["Pedestrian"]["pedestrianCategory"])
                    BoundingBox = ET.SubElement(Pedestrian, "BoundingBox")
                    Center = ET.SubElement(BoundingBox, "Center")
                    Center.set("x", npc["Center"]["x"])
                    Center.set("y", npc["Center"]["y"])
                    Center.set("z", npc["Center"]["z"])
                    Dimensions = ET.SubElement(BoundingBox, "Dimensions")
                    Dimensions.set("width", npc["Dimensions"]["width"])
                    Dimensions.set("length", npc["Dimensions"]["length"])
                    Dimensions.set("height", npc["Dimensions"]["height"])
                    Properties = ET.SubElement(Pedestrian, "Properties")
                    Property = ET.SubElement(Properties, "Property")
                    Property.set("name", "type")
                    Property.set("value", "simulation")
        return
