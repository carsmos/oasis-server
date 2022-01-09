from abc import ABC, abstractmethod
from sdgApp.Domain.dynamic_scenes.dynamic_scenes import ScenariosAggregate


class ScenariosRepo(ABC):

    @abstractmethod
    def create_scenario(self, scenario: ScenariosAggregate):
        raise NotImplementedError

    @abstractmethod
    def find_specified_scenario(self, scenario_id: str):
        raise NotImplementedError

    @abstractmethod
    def find_all_scenario(self):
        raise NotImplementedError

    @abstractmethod
    def update_scenario(self, scenario_id: str, scenario: ScenariosAggregate):
        raise NotImplementedError

    @abstractmethod
    def delete_scenario_by_id(self, scenario_id: str):
        raise NotImplementedError
