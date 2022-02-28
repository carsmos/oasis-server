from abc import ABC, abstractmethod

class LogRepo(ABC):

    @abstractmethod
    def list(self, task_id: str, level: str):
        raise NotImplementedError