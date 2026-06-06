from abc import abstractmethod, ABC

from src.interface_adapters.dtos.task import TaskDto


class TaskQueuePublisherInterface(ABC):
    def __init__(self, connection) -> None:
        self.connection = connection

    @abstractmethod
    async def publish(self, task_id: TaskDto) -> None:
        pass
