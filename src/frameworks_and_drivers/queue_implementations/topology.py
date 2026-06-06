import aio_pika
from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractQueue

from src.entities.task import TaskPriority

EXCHANGE_NAME = "tasks.direct"
QUORUM_QUEUE_ARGS = {"x-queue-type": "quorum"}


def queue_for_priority(priority: TaskPriority) -> str:
    return f"tasks.{priority.value.lower()}"


async def setup_topology(channel: AbstractChannel) -> AbstractExchange:
    exchange = await channel.declare_exchange(
        EXCHANGE_NAME,
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )
    for priority in TaskPriority:
        queue = await channel.declare_queue(
            queue_for_priority(priority),
            durable=True,
            arguments=QUORUM_QUEUE_ARGS,
        )
        await queue.bind(exchange, routing_key=priority.value)
    return exchange


async def setup_worker_queue(
    channel: AbstractChannel,
    queue_name: str,
) -> AbstractQueue:
    exchange = await channel.declare_exchange(
        EXCHANGE_NAME,
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )
    queue = await channel.declare_queue(
        queue_name,
        durable=True,
        arguments=QUORUM_QUEUE_ARGS,
    )
    routing_key = queue_name.removeprefix("tasks.").upper()
    await queue.bind(exchange, routing_key=routing_key)
    return queue
