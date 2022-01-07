from abc import ABC, abstractmethod
from sdgApp.Domain.envs.envs import EnvsAggregate


class EnvsRepo(ABC):

    @abstractmethod
    def create(self, env: EnvsAggregate):
        raise NotImplementedError

    # @abstractmethod
    # def find_by_id(self, id: str):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def update(self, env: EnvsAggregate):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def delete_by_id(self, id: str):
    #     raise NotImplementedError
