from abc import abstractmethod, ABC

from src.interface_adapters.dtos.task import TaskDto, TasksPageDto
from src.entities.task import TaskStatus


class TaskStorageInterface(ABC):
    @abstractmethod
    async def create_task(self, task: TaskDto) -> TaskDto:
        pass

    @abstractmethod
    async def get_tasks(
        self,
        page: int,
        page_size: int,
        status: TaskStatus | None = None,
    ) -> TasksPageDto:
        pass

    @abstractmethod
    async def get_task_by_id(self, task_id: int) -> TaskDto:
        pass

    @abstractmethod
    async def delete_task(self, task_id: int) -> bool:
        pass

    @abstractmethod
    async def get_task_status(self, task_id: int) -> TaskStatus:
        pass

    @abstractmethod
    async def update_task_start(self, task_id: int) -> TaskStatus:
        pass

    @abstractmethod
    async def update_task_end(
        self, task_id: int, result_task: dict, error_info: dict
    ) -> TaskStatus:
        pass

    @abstractmethod
    async def commit(self) -> bool:
        pass
