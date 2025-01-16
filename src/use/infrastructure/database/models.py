from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    Integer,
    LargeBinary,
    MetaData,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import registry

from use.entities.task.models import Task, TaskCompleted
from use.entities.user.models import User

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)
mapper_registry = registry(metadata=metadata)


users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(25), nullable=False, unique=True),
    Column("hashed_password", LargeBinary, nullable=False),
    Column("role", String(10), nullable=False),
    Column("is_active", Boolean, nullable=False, default=True),
    Column(
        "created_at",
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    ),
    Column(
        "updated_at",
        TIMESTAMP,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    ),
)

tasks_table = Table(
    "tasks",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("type", Integer, nullable=False),
    Column("body", Text, nullable=False),
    Column("answer", String, nullable=False),
    Column("time_limit", Integer, nullable=False),
    Column(
        "created_at",
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    ),
    Column(
        "updated_at",
        TIMESTAMP,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    ),
)

completed_tasks_table = Table(
    "completed_tasks",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("task_id", Integer, nullable=False),
    Column("user_id", Integer, nullable=False),
    Column("code", String(555), nullable=False),
    Column("completed_time", Integer, nullable=False),
    Column(
        "created_at",
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    ),
    Column(
        "updated_at",
        TIMESTAMP,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    ),
)


def map_tables() -> None:
    mapper_registry.map_imperatively(User, users_table)
    mapper_registry.map_imperatively(Task, tasks_table)
    mapper_registry.map_imperatively(TaskCompleted, completed_tasks_table)
