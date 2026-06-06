from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection

from src.frameworks_and_drivers.queue_implementations.settings import rabbitmq_settings

_rabbitmq_connection: AbstractRobustConnection | None = None


async def init_rabbitmq_connection() -> AbstractRobustConnection:
    global _rabbitmq_connection
    if _rabbitmq_connection is None or _rabbitmq_connection.is_closed:
        _rabbitmq_connection = await connect_robust(rabbitmq_settings.url)
    return _rabbitmq_connection


async def close_rabbitmq_connection() -> None:
    global _rabbitmq_connection
    if _rabbitmq_connection is not None and not _rabbitmq_connection.is_closed:
        await _rabbitmq_connection.close()
    _rabbitmq_connection = None


def get_rabbitmq_connection() -> AbstractRobustConnection:
    if _rabbitmq_connection is None or _rabbitmq_connection.is_closed:
        raise RuntimeError("RabbitMQ connection is not initialized")
    return _rabbitmq_connection
