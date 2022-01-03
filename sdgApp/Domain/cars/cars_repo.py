from abc import ABC, abstractmethod
from sdgApp.Domain.cars.cars import CarsAggregate

class CarsRepo(ABC):

    @abstractmethod
    def create(self, car: CarsAggregate):
        raise NotImplementedError

    # @abstractmethod
    # def find_by_id(self, id: str) -> Optional[CarsAggregate]:
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def update(self, car: CarsAggregate):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def delete_by_id(self, id: str):
    #     raise NotImplementedError