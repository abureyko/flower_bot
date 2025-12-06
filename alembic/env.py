import asyncio
import os
import sys
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import create_engine
from alembic import context

# Подключаем приложение
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db import Base
import app.models  # важно

config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

# Берём async URL и конвертируем в sync
ASYNC_URL = os.getenv("DATABASE_URL")
SYNC_URL = ASYNC_URL.replace("asyncpg", "psycopg2")

def run_migrations_offline():
    context.configure(
        url=SYNC_URL,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(SYNC_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()