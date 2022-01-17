from abc import ABC, abstractmethod
from sdgApp.Domain.car.car import CarAggregate

class CarRepo(ABC):

    @abstractmethod
    def create(self, car: CarAggregate):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def update_snap(self, snapshot_car: CarAggregate):
        raise NotImplementedError

    @abstractmethod
    def update(self, car: CarAggregate):
        raise NotImplementedError

    @abstractmethod
    def get(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def list(self):
        raise NotImplementedError