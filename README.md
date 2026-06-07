# cism

Сервис асинхронных задач: FastAPI, PostgreSQL, RabbitMQ, Redis, воркеры с приоритетными очередями.

## 1. Настройка переменных окружения

Файлы лежат в `environments/`:

| Файл | Назначение |
|---|---|
| `db.env` | PostgreSQL и PgBouncer |
| `rabbitmq.env` | URL RabbitMQ |
| `redis.env` | URL Redis и TTL кэша статусов |
| `model.env` | OpenRouter API (для LLM-воркеров) |

Перед запуском **обязательно** укажите свой ключ OpenRouter в `environments/model.env`:

```env
OPENROUTER_API_KEY=your-api-key-here
```

При необходимости измените пароль БД в `environments/db.env` и синхронизируйте его с `docker/pgbouncer/userlist.txt`.

## 2. Docker-сеть

В `docker-compose.yml` используется внешняя сеть `cism`. Создайте её один раз:

```bash
docker network create cism
```

## 3. Запуск инфраструктуры

Сначала поднимите базу данных и дождитесь её готовности:

```bash
docker compose up -d db redis pgbouncer rabbitmq-1 rabbitmq-2 rabbitmq-3 rabbitmq
```

RabbitMQ-кластер (3 ноды + HAProxy) стартует 1–2 минуты. Проверить статус:

```bash
docker compose ps
```

## 4. Миграции базы данных

Установите зависимости и примените миграции **с хоста** (PostgreSQL доступен на порту `5532`):

```bash
uv sync --group dev

POSTGRES_DIRECT_HOST=localhost \
POSTGRES_DIRECT_PORT=5532 \
uv run python -m alembic \
  -c src/frameworks_and_drivers/repositories_implementations/aync_sqlalchemy/alembic.ini \
  upgrade head
```

## 5. Запуск приложения

Соберите образы и поднимите все сервисы с масштабированием:

```bash
docker compose up -d --build \
  --scale fastapi=3 \
  --scale worker-high=3 \
  --scale worker-medium=2 \
  --scale worker-low=1
```

### Что поднимается

| Сервис | Назначение |
|---|---|
| `nginx` | Балансировщик, порт **80** |
| `fastapi` | HTTP API (за nginx) |
| `worker-high/medium/low` | Обработчики очередей по приоритету |
| `db` | PostgreSQL 15, порт **5532** (host) |
| `pgbouncer` | Пул соединений к БД |
| `redis` | Кэш статусов задач |
| `rabbitmq` | HAProxy → кластер RabbitMQ, порт **5672** |
| `rabbitmq-1` | Management UI, порт **15672** |

## 6. Проверка работы

API доступен на `http://localhost`.

Создать задачу:

```bash
curl -s -X POST http://localhost/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "name": "demo-task",
    "description": "Hello from cism",
    "priority": "MEDIUM",
    "type_task": "CPU",
    "status": "NEW"
  }'
```

Список задач:

```bash
curl -s "http://localhost/tasks?page=1&page_size=20"
```

Статус задачи (подставьте `task_id` из ответа создания):

```bash
curl -s http://localhost/tasks/1/status
```

Документация API: `http://localhost/docs`

Логи воркеров:

```bash
docker compose logs -f worker-high
```

## 7. Локальная разработка без Docker

Для запуска API на хосте нужны работающие PostgreSQL, Redis и RabbitMQ (через Docker или локально).

```bash
uv sync --group dev

# при запущенном docker compose с проброшенными портами:
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5532
export REDIS_URL=redis://localhost:6379/0
export RABBITMQ_URL=amqp://guest:guest@localhost:5672/

uv run uvicorn src.frameworks_and_drivers.http_web_fastapi.main:app \
  --reload --host 0.0.0.0 --port 8000
```

Воркер локально:

```bash
RABBITMQ_QUEUE_NAME=tasks.high \
uv run python -m src.frameworks_and_drivers.queue_implementations.consumer.consumer
```

## 8. Тесты

```bash
uv sync --group dev

# все тесты (SQLite + unit + API)
uv run pytest

# только интеграционные тесты на реальной PostgreSQL
# (нужен запущенный docker compose с db на порту 5532)
uv run pytest -m postgres -v
```

Pre-commit (линтеры и форматирование):

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## 9. Остановка и очистка

Остановить сервисы:

```bash
docker compose down
```

Удалить контейнеры и volumes (данные БД и RabbitMQ будут потеряны):

```bash
docker compose down -v
```
