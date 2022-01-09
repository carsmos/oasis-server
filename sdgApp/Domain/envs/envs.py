

class EnvsAggregate(object):
    def __init__(self,
                 env_id=None,
                 env_name=None,
                 desc=None,
                 create_time=None,
                 wetness=None,
                 cloudiness=None,
                 fog_density=None,
                 fog_falloff=None,
                 fog_distance=None,
                 precipitation=None,
                 wind_intensity=None,
                 sun_azimuth_angle=None,
                 sun_altitude_angle=None,
                 precipitation_deposits=None,
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
