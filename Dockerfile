# --- Базовый образ ---
FROM python:3.11-slim

# --- Рабочая директория ---
WORKDIR /app

# --- Установка системных зависимостей ---
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# --- Копируем зависимости ---
COPY requirements.txt .

# --- Устанавливаем зависимости ---
RUN pip install --no-cache-dir -r requirements.txt

# --- Копируем весь проект ---
COPY . .

# --- Делаем entrypoint.sh исполняемым ---
RUN chmod +x ./entrypoint.sh

# --- Запуск через entrypoint ---
ENTRYPOINT ["./entrypoint.sh"]
