from abc import ABC, abstractmethod
from sdgApp.Domain.sensorlib import sensor_aggregate

class SensorRepo(ABC):

    @abstractmethod
    def create(self, sensor:sensor_aggregate):
        raise NotImplementedError