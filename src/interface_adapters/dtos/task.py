from datetime import datetime

from pydantic import BaseModel, Field

from src.entities.task import TaskPriority, TaskStatus, TypeTask


class TaskDto(BaseModel):
    task_id: int | None = None
    name: str
    description: str
    priority: TaskPriority
    type_task: TypeTask = TypeTask.CPU
    status: TaskStatus
    created_at: datetime | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    result: dict = {}
    info: dict = {}


class TasksPageDto(BaseModel):
    items: list[TaskDto]
    total: int
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
