from abc import ABC, abstractmethod
from sdgApp.Domain.wheel.wheel import WheelAggregate

class WheelRepo(ABC):

    @abstractmethod
    def create(self, wheel: WheelAggregate):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def update(self, wheel: WheelAggregate):
        raise NotImplementedError

    @abstractmethod
    def get(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def list(self, query_param: dict):
        raise NotImplementedError