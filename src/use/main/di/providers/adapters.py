import os
from collections.abc import AsyncIterator
from typing import NewType

from dishka import (
    AnyOf,
    Provider,
    Scope,
    provide,
)
from faststream.rabbit import RabbitBroker
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from use.application.auth.protocols import JWTManageProtocol
from use.application.broker_publisher.protocol import (
    BrokerUSEPublisherProtocol,
)
from use.application.cache.protocol import CacheProtocol
from use.application.common.protocols.uow import UoWProtocol
from use.application.cookie.interactor import CookieManagerInteractor
from use.application.task.protocols import TaskCreateProtocol, TaskReadProtocol
from use.application.task.protocols.update import TaskUpdateProtocol
from use.application.user.protocols import (
    PasswordHasherProtocol,
    UserCreateProtocol,
    UserReadProtocol,
    UserUpdateProtocol,
)
from use.infrastructure.auth.repositories import AccessManagerRepository
from use.infrastructure.broker_publisher.repository import BrokerUSEPublisher
from use.infrastructure.cache.repository import CacheRepository
from use.infrastructure.cookie.repositories import (
    CookieAccessManagerRepository,
)
from use.infrastructure.task.repositories.add import TaskCreateRepository
from use.infrastructure.task.repositories.read import TaskReadRepository
from use.infrastructure.task.repositories.update import TaskUpdateRepository
from use.infrastructure.user.repositories import (
    PasswordHasherRepository,
    UserCreateRepository,
    UserReadRepository,
    UserUpdateRepository,
)
from use.main.config import Config, create_config

DBURI = NewType("DBURI", str)


class DBProvider(Provider):
    @provide(scope=Scope.APP)
    def db_uri(self) -> DBURI:
        db_uri = os.getenv("DB_URI")
        if db_uri is None:
            error_message = "DB_URI is not set"
            raise ValueError(error_message)
        return DBURI(db_uri)

    @provide(scope=Scope.APP)
    async def create_engine(self, db_uri: DBURI) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(
            db_uri,
            echo=False,
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def create_async_sessionmaker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine,
            autoflush=False,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def new_async_session(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AnyOf[AsyncSession, UoWProtocol]]:
        async with session_factory() as session:
            yield session


def repository_provider() -> Provider:
    provider = Provider()
    provider.provide(
        UserCreateRepository,
        scope=Scope.REQUEST,
        provides=UserCreateProtocol,
    )
    provider.provide(
        PasswordHasherRepository,
        scope=Scope.APP,
        provides=PasswordHasherProtocol,
    )
    provider.provide(
        UserReadRepository,
        scope=Scope.REQUEST,
        provides=UserReadProtocol,
    )
    provider.provide(
        UserUpdateRepository,
        scope=Scope.REQUEST,
        provides=UserUpdateProtocol,
    )
    provider.provide(
        AccessManagerRepository,
        scope=Scope.APP,
        provides=JWTManageProtocol,
    )
    provider.provide(
        CookieAccessManagerRepository,
        scope=Scope.REQUEST,
        provides=CookieManagerInteractor,
    )
    provider.provide(
        TaskCreateRepository,
        scope=Scope.REQUEST,
        provides=TaskCreateProtocol,
    )

    provider.provide(
        TaskReadRepository,
        scope=Scope.REQUEST,
        provides=TaskReadProtocol,
    )

    provider.provide(
        TaskUpdateRepository,
        scope=Scope.REQUEST,
        provides=TaskUpdateProtocol,
    )
    provider.provide(
        CacheRepository,
        scope=Scope.APP,
        provides=CacheProtocol,
    )

    provider.provide(
        BrokerUSEPublisher,
        scope=Scope.APP,
        provides=BrokerUSEPublisherProtocol,
    )

    return provider


def create_rabbit_broker() -> RabbitBroker:
    return RabbitBroker()


def create_redis_client() -> Redis:
    return Redis()


def config_provider() -> Provider:
    provider = Provider()
    provider.provide(create_config, scope=Scope.APP, provides=Config)

    return provider


def broker_provider() -> Provider:
    provider = Provider()
    provider.provide(
        create_rabbit_broker, scope=Scope.APP, provides=RabbitBroker
    )

    return provider


def cache_provider() -> Provider:
    provider = Provider()
    provider.provide(create_redis_client, scope=Scope.APP, provides=Redis)

    return provider


def get_adapters_providers() -> list[Provider]:
    return [
        DBProvider(),
        repository_provider(),
        config_provider(),
        broker_provider(),
        cache_provider(),
    ]
