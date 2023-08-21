#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: renpf
# email:renpengfei@guardstrike.com
# datetime: 20220817
import math
# from utils.logger_utils import LogWrapper
import traceback

# loggerd = LogWrapper(server_name="oasis-server").getlogger()


def pretty_xml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将element转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作


def translate_cloud(cloudiness):  # 0-100
    """
    :param cloudiness: string. string formant of cloudiness.
    :return: string. class of cloud type.
    """
    if int(cloudiness) < 25:
        return "free"
    elif 25 <= int(cloudiness) < 50:
        return "cloudy"
    elif 50 <= int(cloudiness) < 75:
        return "overcast"
    elif 75 <= int(cloudiness) <= 100:
        return "rainy"


def translate_fog(fog_density):  # 0-100
    """
    :param fog_density: string. string formant of fog_density.
    :return: string. string formant of visualRange.
    """
    clear_visualRange = 3000.0
    if int(fog_density) < 1:
        visualRange = clear_visualRange
    else:
        visualRange = clear_visualRange / int(fog_density)
    return str(visualRange)


def translate_precipitation(precipitation_intensity):  # 0-1
    """
    :param precipitation_intensity: rainfall
    :param intensity: string. string formant of precipitation_intensity.
    :return: string. string formant of precipitation intensity and precipitation type.
    """
    if float(precipitation_intensity) > 0.1:
        return "rain"
    else:
        return "dry"


def translate_sun(sun_azimuth_angle, sun_altitude_angle):
    """
    :param sun_azimuth_angle: string. degree of sun_azimuth_angle.
    :param sun_altitude_angle: string. degree of sun_altitude_angle.
    :return: string. rad of sun_azimuth_angle and sun_altitude_angle.
    """
    return str(float(sun_azimuth_angle) / 180.0 * math.pi), str(float(sun_altitude_angle) / 180.0 * math.pi)


def translate_hpr(str_dgr):
    """
    :param str_dgr: string. ui degree of hpr angle.
    :return: string. rad of hpr angle.
    """
    dgr = float(str_dgr)
    rad = dgr / 180.0 * math.pi
    return str(rad)


def generate_datetime(sun_altitude_angle):
    """
    :param sun_altitude_angle: string. rad of sun_altitude_angle
    :return: string. datetime of corresponding sun_altitude_angle.
    """
    date = "2020-09-"
    date_num = 23
    rad = float(sun_altitude_angle)
    second_per_rad = 6 * 60 * 60 / (math.pi / 2.0)  # -pi/2 is 0am, 0 is 6am, pi/2 is 12am
    if rad < math.pi * (-0.5):  # yestoday's 18pm-24pm
        date_num -= 1
        duration = int(second_per_rad * (rad - (-1) * math.pi))
        h = duration // 3600
        m = (duration - 3600 * h) // 60
        s = duration - 3600 * h - 60 * m
        date_time = date + str(date_num) + "T" + str(18 + h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)
    else:
        duration = int(second_per_rad * (rad - (-0.5) * math.pi))
        h = duration // 3600
        m = (duration - 3600 * h) // 60
        s = duration - 3600 * h - 60 * m
        date_time = date + str(date_num) + "T" + str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)
    return date_time


def generate_sun_intensity(date_time, cloudstate):
    """
    :param date_time: string. datetime affecting sun_intensity.
    :param cloudstate: string. cloudstate affecting sun_intensity.
    :return: string. sun_intensity.
    """
    cloudstate_factor = {"skyOff": 1, "free": 1, "cloudy": 0.5, "overcast": 0.2, "rainy": 0.1}
    h = int(date_time[-8:-6])
    if h < 5 or h >= 20:
        return str(10)
    elif (5 <= h < 7) or (18 <= h < 20):  # standard th is 20000
        return str(20000.0 * cloudstate_factor[cloudstate])
    else:  # standard th is 50000
        return str(50000.0 * cloudstate_factor[cloudstate])


def catch_exception(func):
    """
    global error processing, catch error information
    :param func:
    :return: error msg
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # loggerd.error(traceback.format_exc())
            raise e
    return wrapper
