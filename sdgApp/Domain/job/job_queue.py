from abc import ABC, abstractmethod
from sdgApp.Domain.job.job import JobAggregate

class JobQueue(ABC):

    @abstractmethod
    def publish(self, job: JobAggregate):
        raise NotImplementedError