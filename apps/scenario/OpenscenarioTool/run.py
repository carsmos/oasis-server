#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: renpf
# datetime: 20220823
from osxcgenerator import XoscGenerator
import sys
import json

if __name__ == "__main__":
    # json_file_path = sys.argv[1]
    # og = OxscGenerator(json_file_path)
    xg = XoscGenerator(r"./follow_car_modify_weather.json", r"./Catalogs/Vehicles/VehicleCatalog.xosc")
    xosc_file = xg.generate_whole_file()
