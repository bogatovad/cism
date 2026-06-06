from src.entities.task import TaskStatus


class TaskStatusCacheInterface:
    async def get_task_status(self, task_id: int) -> TaskStatus | None:
        pass

    async def set_task_status(self, task_id: int, status: TaskStatus) -> None:
        pass
