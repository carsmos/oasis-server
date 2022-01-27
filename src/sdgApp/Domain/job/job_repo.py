from abc import ABC, abstractmethod
from sdgApp.Domain.job.job import JobAggregate

class JobRepo(ABC):

    @abstractmethod
    def create(self, job: JobAggregate):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def update(self, job: JobAggregate):
        raise NotImplementedError

    @abstractmethod
    def get(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def list(self):
        raise NotImplementedError