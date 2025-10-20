import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Добавьте импорт ваших моделей и Base
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.database import Base
from models.user_model import User
from models.profile_model import Profile
from models.track_model import Track
from models.likes_model import Likes

# config - это объект конфигурации Alembic
config = context.config

# Настройка логирования
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    """Запуск миграций в оффлайн режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Запуск миграций в онлайн режиме."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
