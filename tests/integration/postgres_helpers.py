import os
import uuid

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.frameworks_and_drivers.repositories_implementations.aync_sqlalchemy.models import (
    Task as TaskModel,
)

DEFAULT_TEST_DATABASE_URL = "postgresql+asyncpg://cism:password@localhost:5532/cism"


def postgres_test_url() -> str:
    return os.getenv("TEST_DATABASE_URL", DEFAULT_TEST_DATABASE_URL)


async def delete_tasks(session: AsyncSession, task_ids: list[int]) -> None:
    if not task_ids:
        return
    await session.execute(delete(TaskModel).where(TaskModel.task_id.in_(task_ids)))
    await session.commit()


def unique_task_name(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"
