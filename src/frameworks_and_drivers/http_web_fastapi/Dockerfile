FROM python:3.13-alpine as base

WORKDIR /app

ENV PYTHONPATH=/app \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

# ---- Release ----
FROM base AS release

RUN apk update && pip install uv

# Копируем исходный код приложения
COPY . /app/

# Создание директорий для статических файлов (если нужно)
RUN mkdir -p static && chown 33:33 static

EXPOSE 8000

# Запуск FastAPI с Uvicorn
CMD ["uv", "run", "uvicorn", "src.frameworks_and_drivers.http_web_fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
