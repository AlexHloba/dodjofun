from logging.config import fileConfig
import os
import sys
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

# Подключаем app/
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import Base  # noqa

# Alembic Config
config = context.config

# Настраиваем логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# URL базы
def get_url():
    return os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/dojorise")

# Устанавливаем URL в конфиг Alembic
config.set_main_option("sqlalchemy.url", get_url())

target_metadata = Base.metadata

# --- режимы ---
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    section = config.get_section(config.config_ini_section) or {}
    section["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# Запуск
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
