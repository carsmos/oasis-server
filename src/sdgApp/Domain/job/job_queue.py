from abc import ABC, abstractmethod

class JobQueue(ABC):

    @abstractmethod
    def publish(self, job: dict):
        raise NotImplementedError

    def add(self, job: dict, task_id):
        raise NotImplementedError

    def delete(self, job: dict):
        raise NotImplementedError