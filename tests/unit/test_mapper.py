import pytest
from datetime import datetime
from uuid import UUID
from app.domains import PartDomain, TestDomain
from app.mappers import PartEntityDomainMapper, TestEntityDomainMapper
from app.models import Part, Test


class TestPartEntityDomainMapper:
    @pytest.fixture(autouse=True)
    def _setup_domain(self):
        """
        Set up a TestDomain instance with predefined values
        for testing purposes.
        """
        self._domain = PartDomain(
            id=UUID("00000000-0000-0000-0000-000000000000"),
            name="premium",
            modified_timestamp=datetime(2021, 1, 1),
        )

    @pytest.fixture(autouse=True)
    def _setup_entity(self):
        """
        Set up a TestDomain instance with predefined values
        for testing purposes.
        """
        self._entity = Part(
            id=UUID("00000000-0000-0000-0000-000000000000"),
            name="standard",
            modified_timestamp=datetime(2021, 1, 2),
        )

    @pytest.fixture(autouse=True)
    def _setup_mapper(self):
        self._mapper = PartEntityDomainMapper()

    def test_to_domain(self):
        """
        Test the to_domain method of the PartEntityDomainMapper class.
        """
        domain = self._mapper.to_domain(self._entity)
        assert domain.id == UUID("00000000-0000-0000-0000-000000000000")
        assert domain.name == "standard"
        assert domain.modified_timestamp == datetime(2021, 1, 2)

    def test_to_entity(self):
        """
        Test the to_entity method of the PartEntityDomainMapper class.
        """
        entity = self._mapper.to_entity(self._domain)
        assert entity.id == UUID("00000000-0000-0000-0000-000000000000")
        assert entity.name == "premium"
        assert entity.modified_timestamp == datetime(2021, 1, 1)

    def test_to_entity_with_modified_timestamp(self):
        """
        Test the to_entity method of the PartEntityDomainMapper class.
        """

        self._mapper.map_to_record(self._domain, self._entity)
        assert self._entity.id == UUID("00000000-0000-0000-0000-000000000000")
        assert self._entity.name == "premium"
        assert self._entity.modified_timestamp == datetime(2021, 1, 1)


class TestTestEntityMapper:
    @pytest.fixture(autouse=True)
    def _setup_domain(self):
        """
        Set up a TestDomain instance with predefined values
        for testing purposes.
        """
        self._domain = TestDomain(
            id=UUID("00000000-0000-0000-0000-000000000000"),
            part_id=UUID("00000000-0000-0000-0000-000000000001"),
            timestamp=datetime(2021, 1, 1),
            successful=True,
            data={"type": "premium"},
        )

    @pytest.fixture(autouse=True)
    def _setup_entity(self):
        """
        Set up a TestDomain instance with predefined values
        for testing purposes.
        """
        self._entity = Test(
            id=UUID("00000000-0000-0000-0000-000000000000"),
            part_id=UUID("00000000-0000-0000-0000-000000000010"),
            timestamp=datetime(2021, 2, 1),
            successful=False,
            data={"type": "standard"},
        )

    @pytest.fixture(autouse=True)
    def _setup_mapper(self):
        self._mapper = TestEntityDomainMapper()

    def test_to_domain(self):
        """
        Test the to_domain method of the TestEntityDomainMapper class.
        """
        domain = self._mapper.to_domain(self._entity)
        assert domain.id == UUID("00000000-0000-0000-0000-000000000000")
        assert domain.part_id == UUID("00000000-0000-0000-0000-000000000010")
        assert domain.timestamp == datetime(2021, 2, 1)
        assert domain.successful is False
        assert domain.data == {"type": "standard"}

    def test_to_entity(self):
        """
        Test the to_entity method of the TestEntityDomainMapper class.
        """
        entity = self._mapper.to_entity(self._domain)
        assert entity.id == UUID("00000000-0000-0000-0000-000000000000")
        assert entity.part_id == UUID("00000000-0000-0000-0000-000000000001")
        assert entity.timestamp == datetime(2021, 1, 1)
        assert entity.successful is True
        assert entity.data == {"type": "premium"}

    def test_to_entity_with_modified_timestamp(self):
        """
        Test the to_entity method of the TestEntityDomainMapper class.
        """

        self._mapper.map_to_record(self._domain, self._entity)
        assert self._entity.id == UUID("00000000-0000-0000-0000-000000000000")
        assert self._entity.part_id == UUID(
            "00000000-0000-0000-0000-000000000001"
        )
        assert self._entity.timestamp == datetime(2021, 1, 1)
        assert self._entity.successful is True
        assert self._entity.data == {"type": "premium"}
