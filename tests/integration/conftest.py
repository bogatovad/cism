from collections.abc import AsyncIterator

import pytest
from sqlalchemy import JSON, BigInteger, Integer, event, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.frameworks_and_drivers.repositories_implementations.aync_sqlalchemy.models import (
    Base,
)
from src.frameworks_and_drivers.repositories_implementations.aync_sqlalchemy.task import (
    TaskSqlAlchemyRepository,
)
from tests.integration.postgres_helpers import delete_tasks, postgres_test_url


@event.listens_for(Base.metadata, "before_create")
def _use_sqlite_compatible_types(target, connection, **_kwargs) -> None:
    if connection.dialect.name != "sqlite":
        return

    for table in target.tables.values():
        for column in table.columns:
            if isinstance(column.type, JSONB):
                column.type = JSON()
            if isinstance(column.type, BigInteger) and column.primary_key:
                column.type = Integer()


@pytest.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def task_repository(db_session: AsyncSession) -> TaskSqlAlchemyRepository:
    return TaskSqlAlchemyRepository(db_session)


@pytest.fixture
async def postgres_session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(
        postgres_test_url(),
        pool_pre_ping=True,
        connect_args={"statement_cache_size": 0},
    )
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception as exc:
        await engine.dispose()
        pytest.skip(f"PostgreSQL unavailable: {exc}")

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()

    await engine.dispose()


@pytest.fixture
async def postgres_task_repository(
    postgres_session: AsyncSession,
) -> AsyncIterator[tuple[TaskSqlAlchemyRepository, list[int]]]:
    repository = TaskSqlAlchemyRepository(postgres_session)
    created_task_ids: list[int] = []
    yield repository, created_task_ids
    await delete_tasks(postgres_session, created_task_ids)
