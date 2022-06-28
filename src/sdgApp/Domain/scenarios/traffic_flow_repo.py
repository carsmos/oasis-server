from abc import ABC, abstractmethod

from sdgApp.Application.ScenariosFacadeService.CommandDTOs import TrafficFlow
from sdgApp.Domain.scenarios.scenarios import ScenariosAggregate


class TrafficFlowRepo(ABC):

    @abstractmethod
    def create_traffic_flow(self, scenario_id: str, trafficFlow: TrafficFlow):
        raise NotImplementedError

    @abstractmethod
    def update_traffic_flow(self, traffic_id: str, trafficFlow: TrafficFlow):
        raise NotImplementedError

    @abstractmethod
    def delete_traffic_flow_by_scenario_id(self, scenario_id: str):
        raise NotImplementedError

    @abstractmethod
    def delete_traffic_flow_by_id(self, scenario_id: str):
        raise NotImplementedError

    @abstractmethod
    def get(self, scenario_id: str):
        raise NotImplementedError

    @abstractmethod
    def list(self, scenario_id: str):
        raise NotImplementedError
