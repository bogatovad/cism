from pydantic import BaseModel

from src.entities.task import TaskPriority
from datetime import datetime


class TaskDto(BaseModel):
    name: str
    description: str
    priority: TaskPriority
    status: str
    created_at: datetime
    start_date: datetime
    end_date: datetime
    result: dict
    info: dict
