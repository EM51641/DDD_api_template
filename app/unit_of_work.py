from abc import ABC, abstractmethod
from logging import getLogger

from fastapi import Depends

from app.database import Database
from app.managers import get_db
from app.models import Base
from app.repository import PartRepository, TestRepository
from app.session import Session, SessionEntity

logger = getLogger(__name__)


class BaseUnitOfWork(ABC):
    """
    Base Unit of Work class
    """

    def __init__(
        self,
        session: Session,
        db: Database,
    ) -> None:
        self._session = session
        self._db = db

    @property
    def session(self) -> Session:
        """
        Returns the session object.

        Returns:
            Session: The session object.
        """
        return self._session

    @property
    def db(self) -> Database:
        """
        Returns the database object associated with this unit of work.

        Returns:
            The database object.
        """
        return self._db

    async def save(self) -> None:
        """
        Save all changes persistently.

        Raises:
        ----
            DbException:
                If there is an error saving changes to the
                database.
        """
        try:
            await self._save()
        except Exception as e:
            logger.exception("Error saving changes to the database")
            await self._db.rollback()
            raise e

    async def _save(self) -> None:
        """
        Save all changes persistently.
        """
        await self._process_all_entities()
        await self._commit()

    async def _process_all_entities(self) -> None:
        """
        Add unpersisted data to the database session.
        """
        for entity in self._session.session:
            await self._process_entity(entity)

    async def _process_entity(self, entity: SessionEntity) -> None:
        """
        Processes the given entity based on its operation type.

        Args:
            entity (SessionEntity): The entity to be processed.

        Returns:
            None
        """
        if entity.operation == "add":
            await self._add(entity.entity)
        else:
            await self._remove(entity.entity)

    async def _add(self, entity: Base) -> None:
        """
        Add an entity to the database session.

        Parameters:
        ----
            entity: Base
                The entity to add to the database.

        Raises:
        ----
            AddException:
                If there is an error adding the entity to the database
                session.
        """
        try:
            self._db.add(entity)
        except Exception as e:
            logger.exception("Error adding entity to the database")
            await self._db.rollback()
            raise e

    async def _remove(self, entity: Base) -> None:
        """
        Remove an entity from the database session.

        Parameters:
        ----
            entity: Base
                The entity to remove from the database.

        Raises:
        ----
            RemoveException:
                If there is an error removing the entity from the
                database session.
        """
        try:
            await self._db.remove(entity)
        except Exception as e:
            logger.exception("Error removing entity from the database")
            await self._db.rollback()
            raise e

    async def _commit(self) -> None:
        """
        Commit changes to the database.
        """
        try:
            await self._db.commit()
        except Exception as e:
            logger.exception("Error committing changes to the database")
            await self._db.rollback()
            raise e


class AbstractTestUnitOfWork(BaseUnitOfWork):
    @property
    @abstractmethod
    def part_repository(self) -> PartRepository:
        """Part Repository"""

    @property
    @abstractmethod
    def test_repository(self) -> TestRepository:
        """Test Repository"""


class TestUnitOfWork(AbstractTestUnitOfWork):
    """
    The TestUnitOfWork class is responsible for managing the state of the
    database session and for persisting changes to the database.

    Methods:
    ----
        session: Session
            The database session.
        db: Database
            The database instance.
        part_repository: PartRepository
            The Part Repository.
        test_repository: TestRepository
            The Test Repository.
    """

    def __init__(
        self,
        session: Session = Depends(Session),
        db: Database = Depends(get_db),
    ) -> None:
        super().__init__(session, db)

        self._part_repository = PartRepository(
            db=self._db, session=self._session
        )
        self._test_repository = TestRepository(
            db=self._db, session=self._session
        )

    @property
    def part_repository(self) -> PartRepository:
        """
        Returns the PartRepository instance associated with this UnitOfWork.

        :return: The PartRepository instance.
        """
        return self._part_repository

    @property
    def test_repository(self) -> TestRepository:
        """
        Returns the test repository.

        Returns:
            TestRepository: The test repository object.
        """
        return self._test_repository
