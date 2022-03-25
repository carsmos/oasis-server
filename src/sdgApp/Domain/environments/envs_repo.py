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
    def get(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def list(self):
        raise NotImplementedError
