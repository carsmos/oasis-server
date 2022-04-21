from abc import ABC, abstractmethod

class Run(ABC):

    @abstractmethod
    def publish(self, job: dict):
        raise NotImplementedError