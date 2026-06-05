from src.interface_adapters.dtos.task import TaskDto
from src.entities.task import TaskStatus


# todo: подумать от чего лучше стоит наследоваться. пока оставлю так.
class TaskStorageInterface:
    def create_task(self, task: TaskDto) -> bool:
        pass

    def get_tasks(self) -> list[TaskDto]:
        pass

    def get_task_by_id(self, task_id: int) -> TaskDto:
        pass

    def delete_task(self, task_id: int) -> bool:
        pass

    def get_task_status(self, task_id: int) -> TaskStatus:
        pass
