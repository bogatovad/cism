from src.usecases.base import BaseUseCase


class CreateTaskUseCase(BaseUseCase):
    async def execute(self):
        print("create task use case")


class GetTasksUseCase(BaseUseCase):
    async def execute(self):
        print("get tasks use case")


class GetTaskUseCase(BaseUseCase):
    async def execute(self):
        print("get task use case")


class DeleteTaskUseCase(BaseUseCase):
    async def execute(self):
        print("delete task use case")


class GetStatusTaskUseCase(BaseUseCase):
    async def execute(self):
        print("get status use case")
