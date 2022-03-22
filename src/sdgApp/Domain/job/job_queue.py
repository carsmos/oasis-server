from abc import ABC, abstractmethod

class JobQueue(ABC):

    @abstractmethod
    def publish(self, job: dict):
        raise NotImplementedError