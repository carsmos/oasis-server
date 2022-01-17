from abc import ABC, abstractmethod
from sdgApp.Domain.environments.envs import EnvsAggregate


class EnvsRepo(ABC):

    @abstractmethod
    def create_env(self, env: EnvsAggregate):
        raise NotImplementedError

    @abstractmethod
    def update_env(self, env_id: str, env: EnvsAggregate):
        raise NotImplementedError

    @abstractmethod
    def delete_env(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def find_all_envs(self):
        raise NotImplementedError

    @abstractmethod
    def find_specified_env(self, env_id: str):
        raise NotImplementedError
