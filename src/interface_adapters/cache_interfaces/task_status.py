from abc import abstractmethod, ABC

from src.entities.task import TaskStatus


class TaskStatusCacheInterface(ABC):
    @abstractmethod
    async def get_task_status(self, task_id: int) -> TaskStatus | None:
        pass

    @abstractmethod
    async def set_task_status(self, task_id: int, status: TaskStatus) -> None:
        pass
