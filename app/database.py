from abc import abstractmethod
from functools import cached_property
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
    AsyncEngine,
)
from app.config import Settings
from app.models import Base


class BaseDatabaseApp:
    @property
    @abstractmethod
    def engine(self) -> AsyncEngine | None:
        """Not implemented yet"""

    @property
    @abstractmethod
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        """Not implemented yet"""

    @abstractmethod
    def init_app(self, settings: Settings) -> None:
        """Not implemented yet"""


class DatabaseApp(BaseDatabaseApp):
    """
    A class representing a database connection.

    Properties:
        engine (AsyncEngine | None): The database engine.
        session_maker (async_sessionmaker[AsyncSession]): The session maker object.
    """

    def __init__(self, engine: AsyncEngine | None = None) -> None:
        self._engine = engine
        self._session_maker = self._create_session_maker()

    @cached_property
    def engine(self) -> AsyncEngine | None:
        return self._engine

    @cached_property
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        return self._session_maker

    def init_app(self, settings: Settings) -> None:
        """
        Initializes a new instance of the Database class.

        Args:
            settings (Settings): The settings to use for the database connection.
        """
        self._engine = self._create_engine(settings)
        self._session_maker = self._create_session_maker()

    def _create_engine(self, settings: Settings) -> AsyncEngine:
        """
        Creates an async engine with the given database URI loaded in settings.
        """
        return create_async_engine(settings.DATABASE_URI, pool_pre_ping=True)

    def _create_session_maker(self) -> async_sessionmaker[AsyncSession]:
        """
        Creates an async session maker with the given engine and session settings.

        Returns:
            An async session maker object.
        """
        return async_sessionmaker(
            autocommit=False,
            autoflush=False,
            future=True,
            bind=self._engine,
            expire_on_commit=False,  # settings this as True causes issues in async mode
        )


class BaseDatabase:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session

    @abstractmethod
    def add(self, entity: Base) -> None:
        """Not implemented yet"""

    @abstractmethod
    async def remove(self, entity: Base) -> None:
        """Not implemented yet"""

    @abstractmethod
    async def commit(self) -> None:
        """Not implemented yet"""

    @abstractmethod
    async def rollback(self) -> None:
        """Not implemented yet"""

    @abstractmethod
    async def teardown_session(self) -> None:
        """Not implemented yet"""


class Database(BaseDatabase):
    """
    A class representing a database.

    Methods:
    - add(entity: Base) -> None: Adds an entity to the database session.
    - remove(entity: Base) -> None: Removes an entity from the database session.
    - commit() -> None: Commits the changes made to the database.
    - teardown_session() -> None: Closes the current session.
    """

    def add(self, entity: Base) -> None:
        """
        Adds an entity from the database session.

        Parameters:
        ----
            entity: Base
                The entity to add to the database session.
        """
        self.session.add(entity)

    async def remove(self, entity: Base) -> None:
        """
        Removes an entity from the database session.

        Parameters:
        ----
            entity: Base
                The entity to remove from the database session.
        """
        await self.session.delete(entity)

    async def commit(self) -> None:
        """
        Commits the changes made to the database.
        """
        await self.session.commit()

    async def rollback(self) -> None:
        """
        Flushes pending changes to the database.
        """
        await self.session.rollback()

    async def teardown_session(self) -> None:
        """
        Closes the current session.
        """
        await self._session.close()
