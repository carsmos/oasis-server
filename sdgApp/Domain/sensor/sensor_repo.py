from abc import ABC, abstractmethod
from sdgApp.Domain.sensor.sensor import SensorAggregate

class SensorRepo(ABC):

    @abstractmethod
    def create(self, sensor: SensorAggregate):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def update(self, sensor: SensorAggregate):
        raise NotImplementedError

    @abstractmethod
    def get(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def list(self):
        raise NotImplementedError