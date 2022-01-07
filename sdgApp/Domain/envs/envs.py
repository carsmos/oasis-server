from datetime import datetime
from typing import Optional, Union


class EnvsAggregate(object):
    def __init__(self,
                 env_id: Optional[str],
                 env_name: str,
                 desc: Optional[str],
                 create_time: Union[datetime, str],
                 wetness: float,
                 cloudiness: float,
                 fog_density: float,
                 fog_falloff: float,
                 fog_distance: float,
                 precipitation: float,
                 wind_intensity: float,
                 sun_azimuth_angle: float,
                 sun_altitude_angle: float,
                 precipitation_deposits: float,
                 ):
        self.env_id = env_id
        self.env_name = env_name
        self.create_time = create_time
        self.desc = desc
        self.wetness = wetness
        self.cloudiness = cloudiness
        self.fog_density = fog_density
        self.fog_falloff = fog_falloff
        self.fog_distance = fog_distance
        self.precipitation = precipitation
        self.wind_intensity = wind_intensity
        self.sun_azimuth_angle = sun_azimuth_angle
        self.sun_altitude_angle = sun_altitude_angle
        self.precipitation_deposits = precipitation_deposits

    def save_DO_shortcut(self, dto_dict: dict):
        self.shortcut_DO = dto_dict
