"""
Global Reposiotory
"""
from __future__ import annotations
from functools import cached_property
from typing import Generic, Sequence, TypeVar
from abc import ABC
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.sql.selectable import Select
from sqlalchemy.exc import NoResultFound
from app.database import Database
from app.mappers import (
    BaseEntityDomainMapper,
    PartEntityDomainMapper,
    TestEntityDomainMapper,
)
from app.session import Session
from app.domains import BaseDomain, PartDomain, TestDomain
from app.models import Base, Part, Test
from app.exceptions import NoEntityFoundError

TEntity = TypeVar("TEntity", bound=Base)
TDomain = TypeVar("TDomain", bound=BaseDomain)


class BaseRepository(ABC, Generic[TEntity, TDomain]):
    """
    Repository Pattern.
    """

    def __init__(
        self,
        session: Session,
        db: Database,
        entity_type: type[TEntity],
        mapper: BaseEntityDomainMapper[TEntity, TDomain],
    ) -> None:
        self._entity_type = entity_type
        self._session = session
        self._db = db
        self._mapper = mapper

    @property
    def entity_type(self) -> type[TEntity]:
        return self._entity_type

    @property
    def session(self) -> Session:
        return self._session

    @property
    def db(self) -> Database:
        return self._db

    @property
    def mapper(self) -> BaseEntityDomainMapper[TEntity, TDomain]:
        return self._mapper

    @cached_property
    def _select_table(self) -> Select[tuple[TEntity]]:
        return select(self._entity_type)

    def add(self, domain: TDomain) -> None:
        """
        Add a new domain.

        Params:
        ----
        domain (TDomain): The domain to add.

        Returns:
        ----
        None
        """
        record = self._mapper.to_entity(domain)
        self._session.add(record)

    async def modify(self, domain: TDomain) -> None:
        """
        Modify a domain.

        This method modifies an existing domain by updating its properties
        with the values from the provided domain object.

        Parameters:
            domain (TDomain): The domain object to modify.

        Returns:
            None
        """
        query = self._query_by_id(domain.id)
        record = await self._find_first_record(query)
        self._mapper.map_to_record(domain, record)

    async def remove(self, domain: TDomain) -> None:
        """
        Remove a domain.

        Parameters:
            domain (TDomain): The domain to be removed.

        Returns:
            None
        """
        query = self._query_by_id(domain.id)
        record = await self._find_first_record(query)
        self.session.remove(record)

    async def find_by_id(self, id: UUID) -> TDomain:
        """
        Return the domain by id.

        Params:
        ----
            id: UUID

        Returns:
        ----
            TDomain
        """
        query = self._query_by_id(id)
        domain = await self._find_first_domain(query)
        return domain

    async def find_all(self, limit: int, offset: int) -> list[TDomain]:
        """
        Return all domains.

        Returns:
        ----
            list[TDomain]
        """
        query = self._select_table.limit(limit).offset(offset)
        records = await self._find_all_records(query)
        return [self._mapper.to_domain(record) for record in records]

    async def _find_first_domain(
        self, query: Select[tuple[TEntity]]
    ) -> TDomain:
        """
        Find the first domain.

        Parameters:
        ----
            :param query: query of the oauth.

        Returns:
        ----
            TDomain: The first domain found.
        """
        record = await self._find_first_record(query)
        return self._mapper.to_domain(record)

    async def _find_first_record(
        self, query: Select[tuple[TEntity]]
    ) -> TEntity:
        """
        Find the first record.

        Parameters:
        ----
            :param query: query to get the first record.

        Returns:
        ----
            TEntity: the first record found by the query.
        """
        res = await self._db.session.execute(query)
        try:
            record = res.scalar_one()
        except NoResultFound:
            raise NoEntityFoundError()
        return record

    async def _find_all_records(
        self, query: Select[tuple[TEntity]]
    ) -> Sequence[TEntity]:
        """
        Find all records.

        Parameters:
        ----
            :param query: query to get all records.

        Returns:
        ----
            list[TEntity]: the list of records found by the query.
        """
        res = await self._db.session.execute(query)
        records = res.scalars().all()
        return records

    def _query_by_id(self, id: UUID) -> Select[tuple[TEntity]]:
        """
        Get a query searching a record by id.

        Params:
        ----
            id: UUID - The id of the record to search for.

        Returns:
        ----
           Query[TEntity] - A query object that can be used to search for the record.
        """
        query = self._select_table.filter(self._entity_type.id == id)
        return query


class PartRepository(BaseRepository[Part, PartDomain]):
    """
    Repository class for managing Part entities.

    This class provides methods for interacting with the database and performing CRUD operations on Part entities.

    Args:
        db (Database): The database connection.
        session (Session): The database session.

    """

    def __init__(self, db: Database, session: Session) -> None:
        super().__init__(
            db=db,
            session=session,
            entity_type=Part,
            mapper=PartEntityDomainMapper(),
        )


class TestRepository(BaseRepository[Test, TestDomain]):
    """
    Repository class for managing Test entities.

    This class provides methods for interacting with the database and performing CRUD operations on Test entities.

    Args:
        db (Database): The database connection.
        session (Session): The database session.

    Attributes:
        db (Database): The database connection.
        session (Session): The database session.
        entity_type (Type[Test]): The type of the entity.
        mapper (Mapper[Test, TestDomain]): The mapper for mapping between entity and domain models.
    """

    def __init__(self, db: Database, session: Session) -> None:
        super().__init__(
            db=db,
            session=session,
            entity_type=Test,
            mapper=TestEntityDomainMapper(),
        )
