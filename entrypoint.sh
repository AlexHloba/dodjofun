#!/bin/bash
set -e

echo "🗄️  Применяем миграции Alembic..."
alembic upgrade head || {
  echo "⚠️  Alembic миграции не выполнены, возможно база не готова. Пробуем позже."
  sleep 5
  alembic upgrade head
}

echo "🚀 Запускаем FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
