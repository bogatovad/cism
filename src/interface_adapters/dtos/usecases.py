from dataclasses import dataclass

from src.usecases.task import (
    CreateTaskUseCase,
    GetTaskUseCase,
    GetTasksUseCase,
    DeleteTaskUseCase,
    GetStatusTaskUseCase,
)


@dataclass
class UsecaseDto:
    create_task_usecase: CreateTaskUseCase
    get_tasks_usecase: GetTasksUseCase
    get_task_usecase: GetTaskUseCase
    delete_task_usecase: DeleteTaskUseCase
    get_status_usecase: GetStatusTaskUseCase
