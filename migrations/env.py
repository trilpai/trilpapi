from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from src.core.config import settings
from src.models.base import Base
from src.features.offices.models.offices import Office
from src.features.users.models.privileges import Privilege
from src.features.users.models.roles import Role
from src.features.users.models.role_privileges import RolePrivilege
from src.features.users.models.users import User
from src.features.users.models.refresh_tokens import RefreshToken
from src.features.users.models.user_activity import UserActivity
# Add imports for additional models here as needed

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support.
target_metadata = Base.metadata  # Use the Base metadata for models

# Dynamically set the database URL using settings
config.set_main_option("sqlalchemy.url", settings.database_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation,
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string
    to the script output.
    """
    url = settings.database_url
    print(f"Running migrations offline with URL: {url}")  # Debug
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    This scenario creates an Engine and associates a connection with the context.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def do_run_migrations():
        """Execute migrations asynchronously."""
        async with connectable.connect() as connection:
            # Configure the migration context
            await connection.run_sync(
                lambda conn: context.configure(
                    connection=conn,
                    target_metadata=target_metadata,
                )
            )

            # Execute the migrations
            await connection.run_sync(lambda _: context.run_migrations())

    import asyncio

    asyncio.run(do_run_migrations())


# Determine whether to run in offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()