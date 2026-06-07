from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from src.entities.task import TaskStatus
from src.interface_adapters.dtos.task import TasksPageDto
from src.usecases.usecases_api.task import (
    CreateTaskUseCase,
    DeleteTaskUseCase,
    GetTaskUseCase,
    GetTasksUseCase,
)
from tests.fakes.repository import sample_task_dto


def _created_task(task_id: int = 1):
    return sample_task_dto().model_copy(
        update={
            "task_id": task_id,
            "created_at": datetime.now(UTC),
        }
    )


@pytest.mark.asyncio
async def test_create_task_usecase_publishes_and_caches() -> None:
    repository = AsyncMock()
    queue = AsyncMock()
    cache = AsyncMock()
    created = _created_task()
    repository.create_task.return_value = created

    usecase = CreateTaskUseCase(repository, queue, cache)
    task_input = sample_task_dto()

    result = await usecase.execute(task_input)

    repository.create_task.assert_awaited_once_with(task_input)
    queue.publish.assert_awaited_once_with(created)
    cache.set_task_status.assert_awaited_once_with(created.task_id, created.status)
    assert result == created


@pytest.mark.asyncio
async def test_create_task_usecase_without_cache() -> None:
    repository = AsyncMock()
    queue = AsyncMock()
    created = _created_task()
    repository.create_task.return_value = created

    usecase = CreateTaskUseCase(repository, queue, status_cache=None)
    task_input = sample_task_dto()

    result = await usecase.execute(task_input)

    repository.create_task.assert_awaited_once_with(task_input)
    queue.publish.assert_awaited_once_with(created)
    assert result == created


@pytest.mark.asyncio
async def test_get_tasks_usecase_returns_page() -> None:
    repository = AsyncMock()
    page = TasksPageDto(
        items=[_created_task(1), _created_task(2)],
        total=5,
        page=2,
        page_size=2,
    )
    repository.get_tasks.return_value = page

    usecase = GetTasksUseCase(repository)

    result = await usecase.execute(page=2, page_size=2, status=TaskStatus.NEW)

    repository.get_tasks.assert_awaited_once_with(
        page=2,
        page_size=2,
        status=TaskStatus.NEW,
    )
    assert result == page


@pytest.mark.asyncio
async def test_get_task_usecase() -> None:
    repository = AsyncMock()
    created = _created_task(1)
    repository.get_task_by_id.return_value = created

    usecase = GetTaskUseCase(repository)

    result = await usecase.execute(1)

    repository.get_task_by_id.assert_awaited_once_with(1)
    assert result == created


@pytest.mark.asyncio
async def test_delete_task_usecase_updates_cache() -> None:
    repository = AsyncMock()
    cache = AsyncMock()
    repository.delete_task.return_value = True

    usecase = DeleteTaskUseCase(repository, cache)

    result = await usecase.execute(1)

    repository.delete_task.assert_awaited_once_with(1)
    cache.set_task_status.assert_awaited_once_with(1, TaskStatus.CANCELED)
    assert result is True
