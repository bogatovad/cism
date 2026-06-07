from unittest.mock import AsyncMock

import pytest

from src.entities.task import TaskStatus, TypeTask
from src.usecases.usecases_api.task import (
    CreateTaskUseCase,
    DeleteTaskUseCase,
    GetStatusTaskUseCase,
    GetTaskUseCase,
    GetTasksUseCase,
)
from src.usecases.usecases_logic.task import ProcessCpuTasksUseCase
from tests.fakes.cache import FakeTaskStatusCache
from tests.fakes.queue import FakeTaskQueuePublisher
from tests.fakes.repository import sample_task_dto
from tests.integration.postgres_helpers import unique_task_name

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_api_task_full_cycle_on_postgres(postgres_task_repository) -> None:
    repository, created_task_ids = postgres_task_repository
    queue = FakeTaskQueuePublisher()
    cache = FakeTaskStatusCache()
    task_name = unique_task_name("api-cycle")

    create_usecase = CreateTaskUseCase(repository, queue, cache)
    get_task_usecase = GetTaskUseCase(repository)
    get_status_usecase = GetStatusTaskUseCase(repository, cache)
    get_tasks_usecase = GetTasksUseCase(repository)
    delete_usecase = DeleteTaskUseCase(repository, cache)

    created = await create_usecase.execute(
        sample_task_dto(name=task_name, type_task=TypeTask.CPU)
    )
    await repository.commit()
    created_task_ids.append(created.task_id)

    assert created.task_id is not None
    assert len(queue.published) == 1
    assert queue.published[0].task_id == created.task_id

    fetched = await get_task_usecase.execute(created.task_id)
    assert fetched.name == task_name

    # так как нету отправики в реальную очередь, то задача не переходит в статус IN_PROGRESS.
    assert fetched.status == TaskStatus.NEW

    status = await get_status_usecase.execute(created.task_id)
    assert status == TaskStatus.NEW

    page = await get_tasks_usecase.execute(
        page=1,
        page_size=100,
        status=TaskStatus.NEW,
    )
    assert any(item.task_id == created.task_id for item in page.items)

    deleted = await delete_usecase.execute(created.task_id)
    await repository.commit()
    assert deleted is True

    canceled_status = await repository.get_task_status(created.task_id)
    assert canceled_status == TaskStatus.CANCELED
    assert await cache.get_task_status(created.task_id) == TaskStatus.CANCELED


@pytest.mark.asyncio
async def test_worker_task_full_cycle_on_postgres(
    postgres_task_repository,
    mocker,
) -> None:
    repository, created_task_ids = postgres_task_repository
    cache = FakeTaskStatusCache()
    task_name = unique_task_name("worker-cycle")
    mocker.patch(
        "src.usecases.usecases_logic.task.sleep",
        new_callable=AsyncMock,
    )

    created = await repository.create_task(
        sample_task_dto(name=task_name, type_task=TypeTask.CPU)
    )
    await repository.commit()
    created_task_ids.append(created.task_id)

    process_usecase = ProcessCpuTasksUseCase(repository, cache)

    # Этот юзкейс дергается внутри worker.
    processed = await process_usecase.execute(created)

    assert processed is True

    completed = await repository.get_task_by_id(created.task_id)
    assert completed.status == TaskStatus.COMPLETED
    assert completed.result["type_task"] == "ProcessCpuTasksUseCase"
    assert completed.start_date is not None
    assert completed.end_date is not None
    assert await cache.get_task_status(created.task_id) == TaskStatus.COMPLETED
