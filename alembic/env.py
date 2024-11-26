
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.declarative import declarative_base
from alembic import context
from dotenv import load_dotenv
from app import Base  # Sizning SQLAlchemy modellarini import qilish

# .env faylini o‘qish
load_dotenv()

# Config faylidan ma'lumotlar bazasi URL'ini o'qish
config = context.config
config.set_main_option('sqlalchemy.url', os.getenv("DATABASE_URL"))

# Logging konfiguratsiyasi
fileConfig(config.config_file_name)

# SQLAlchemy modellarini import qilish
target_metadata = Base.metadata

# Offline va Online migratsiyalar uchun funksiyalar
def run_migrations_online():
    # Database connection setup
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    # Offline migrations
    run_migrations_offline()
else:
    # Online migrations
    run_migrations_online()
