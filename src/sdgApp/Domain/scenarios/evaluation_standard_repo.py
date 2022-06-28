from abc import ABC, abstractmethod

from Application.ScenariosFacadeService.CommandDTOs import EvaluationStandard
from sdgApp.Domain.scenarios.scenarios import ScenariosAggregate


class EvaluationStandardRepo(ABC):

    @abstractmethod
    def create_evaluation_standard(self, scenario_id: str, evaluation_standard: EvaluationStandard):
        raise NotImplementedError

    @abstractmethod
    def update_evaluation_standard(self, evaluation_standard: EvaluationStandard):
        raise NotImplementedError

    @abstractmethod
    def delete_evaluation_standard_by_id(self, evaluation_standard_id: str):
        raise NotImplementedError

    @abstractmethod
    def delete_evaluation_standard_by_scenario_id(self, scenario_id: str):
        raise NotImplementedError

    @abstractmethod
    def get(self, id: str):
        raise NotImplementedError
