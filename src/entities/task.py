from enum import Enum
from datetime import datetime


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskStatus(str, Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class Task:
    name: str
    description: str
    priority: TaskPriority
    status: str
    created_at: datetime
    start_date: datetime
    end_date: datetime
    result: dict
    info: dict
