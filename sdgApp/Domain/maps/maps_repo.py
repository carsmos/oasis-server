from abc import ABC, abstractmethod
from sdgApp.Domain.maps.maps import MapsAggregate


class MapsRepo(ABC):

    @abstractmethod
    def find_all_maps(self):
        raise NotImplementedError

    @abstractmethod
    def find_map_by_id(self, map_id: int):
        raise NotImplementedError

    @abstractmethod
    def find_map_by_name(self, name: str):
        raise NotImplementedError
