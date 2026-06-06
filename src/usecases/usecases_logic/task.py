from asyncio import sleep

from src.interface_adapters.dtos.task import TaskDto
from src.interface_adapters.repositories_interfaces.task import TaskStorageInterface
from src.usecases.base import BaseUseCase


class ProcessLllTasksUseCase(BaseUseCase):
    def __init__(self, task_repository: TaskStorageInterface):
        self.task_repository = task_repository

    async def execute(self, task: TaskDto) -> bool:
        await self.task_repository.update_task_start(task_id=task.task_id)
        await self.task_repository.commit()
        print("ProcessLllTasksUseCase")
        result_task = {"result": True, "type_task": "ProcessLllTasksUseCase"}
        await sleep(10)
        await self.task_repository.update_task_end(
            task_id=task.task_id, result_task=result_task
        )
        await self.task_repository.commit()
        return True


class ProcessCpuTasksUseCase(BaseUseCase):
    def __init__(self, task_repository: TaskStorageInterface):
        self.task_repository = task_repository

    async def execute(self, task: TaskDto) -> bool:
        await self.task_repository.update_task_start(task_id=task.task_id)
        await self.task_repository.commit()
        print("ProcessCpuTasksUseCase")
        result_task = {"result": True, "type_task": "ProcessCpuTasksUseCase"}
        await sleep(10)
        await self.task_repository.update_task_end(
            task_id=task.task_id, result_task=result_task
        )
        await self.task_repository.commit()
        return True


class ProcessReadSharedMemoryUseCase(BaseUseCase):
    def __init__(self, task_repository: TaskStorageInterface):
        self.task_repository = task_repository

    async def execute(self, task: TaskDto) -> bool:
        await self.task_repository.update_task_start(task_id=task.task_id)
        await self.task_repository.commit()
        print("ProcessReadSharedMemoryUseCase")
        result_task = {"result": True, "type_task": "ProcessReadSharedMemoryUseCase"}
        await sleep(10)
        await self.task_repository.update_task_end(
            task_id=task.task_id, result_task=result_task
        )
        await self.task_repository.commit()
        return True
