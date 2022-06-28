from abc import ABC, abstractmethod
from sdgApp.Domain.light.lights import LightAggregate


class LightRepo(ABC):

    @abstractmethod
    def create_light(self, light: LightAggregate):
        raise NotImplementedError

    @abstractmethod
    def update_light(self, light_id: str, light: LightAggregate):
        raise NotImplementedError

    @abstractmethod
    def delete_light(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def get(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def list(self):
        raise NotImplementedError
