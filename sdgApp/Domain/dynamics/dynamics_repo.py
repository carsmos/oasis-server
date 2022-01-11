from abc import ABC, abstractmethod
from sdgApp.Domain.dynamics.dynamics import DynamicsAggregate

class DynamicsRepo(ABC):

    @abstractmethod
    def create(self, dynamics: DynamicsAggregate):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def update(self, dynamics: DynamicsAggregate):
        raise NotImplementedError

    @abstractmethod
    def get(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def list(self, query_param: dict):
        raise NotImplementedError