from src.interface_adapters.controllers.task import TaskController
from src.interface_adapters.dtos.usecases import UsecaseDto
from src.usecases.task import (
    CreateTaskUseCase,
    GetTaskUseCase,
    GetStatusTaskUseCase,
    GetTasksUseCase,
    DeleteTaskUseCase,
)


async def task_controller_dependency():
    create_task_usecase = CreateTaskUseCase()
    get_task_usecase = GetTaskUseCase()
    get_status_task_usecase = GetStatusTaskUseCase()
    get_tasks_usecase = GetTasksUseCase()
    delete_task_usecase = DeleteTaskUseCase()

    usecase_dto = UsecaseDto(
        create_task_usecase=create_task_usecase,
        get_task_usecase=get_task_usecase,
        get_status_usecase=get_status_task_usecase,
        delete_task_usecase=delete_task_usecase,
        get_tasks_usecase=get_tasks_usecase,
    )
    task_controller = TaskController(
        usecase=usecase_dto,
    )
    return task_controller
