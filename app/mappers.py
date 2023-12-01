"""
Module for Mappers between entity and domain objects.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.domains import BaseDomain, PartDomain, TestDomain
from app.models import Base, Part, Test

TEntity = TypeVar("TEntity", bound=Base)
TDomain = TypeVar("TDomain", bound=BaseDomain)


class BaseEntityDomainMapper(ABC, Generic[TEntity, TDomain]):
    """
    Abstract base class for entity-domain mappers.
    """

    @abstractmethod
    def to_domain(self, entity: TEntity) -> TDomain:
        """
        Not implemented yet
        """

    @abstractmethod
    def to_entity(self, domain: TDomain) -> TEntity:
        """
        Not implemented yet
        """

    @abstractmethod
    def map_to_record(self, domain: TDomain, record: TEntity) -> None:
        """
        Not implemented yet
        """


class PartEntityDomainMapper(BaseEntityDomainMapper[Part, PartDomain]):
    """
    Mapper for Part entity-domain.
    """

    def to_domain(self, entity: Part) -> PartDomain:
        """
        Converts an entity object to a domain object.

        Args:
            entity (Part): The entity object to be converted.

        Returns:
            PartDomain: The converted domain object.
        """
        return PartDomain(
            id=entity.id,
            name=entity.name,
            modified_timestamp=entity.modified_timestamp,
        )

    def to_entity(self, domain: PartDomain) -> Part:
        """
        Converts a PartDomain object to a Part object.

        Args:
            domain (PartDomain): The PartDomain object to be converted.

        Returns:
            Part: The converted Part object.
        """
        return Part(
            id=domain.id,
            name=domain.name,
            modified_timestamp=domain.modified_timestamp,
        )

    def map_to_record(self, domain: PartDomain, record: Part) -> None:
        """
        Maps the attributes from the PartDomain object to the Part object.

        Args:
            domain (PartDomain): The PartDomain object containing the attributes to be mapped.
            record (Part): The Part object to which the attributes will be mapped.

        Returns:
            None
        """

        assert domain.id == record.id

        record.name = domain.name
        record.modified_timestamp = domain.modified_timestamp


class TestEntityDomainMapper(BaseEntityDomainMapper[Test, TestDomain]):
    """
    Mapper for Test entity-domain.
    """

    def to_domain(self, entity: Test) -> TestDomain:
        """
        Converts an entity object to a domain object.

        Args:
            entity (Test): The entity object to be converted.

        Returns:
            TestDomain: The converted domain object.
        """
        return TestDomain(
            id=entity.id,
            part_id=entity.part_id,
            data=entity.data,
            successful=entity.successful,
            timestamp=entity.timestamp,
        )

    def to_entity(self, domain: TestDomain) -> Test:
        """
        Converts a TestDomain object to a Test object.

        Args:
            domain (TestDomain): The TestDomain object to be converted.

        Returns:
            Test: The converted Test object.
        """
        return Test(
            id=domain.id,
            part_id=domain.part_id,
            data=domain.data,
            successful=domain.successful,
            timestamp=domain.timestamp,
        )

    def map_to_record(self, domain: TestDomain, record: Test) -> None:
        """
        Maps the attributes from a TestDomain object to a Test object.

        Args:
            domain (TestDomain): The TestDomain object containing the attributes to be mapped.
            record (Test): The Test object to which the attributes will be mapped.

        Returns:
            None
        """

        assert domain.id == record.id

        record.part_id = domain.part_id
        record.data = domain.data
        record.successful = domain.successful
        record.timestamp = domain.timestamp
