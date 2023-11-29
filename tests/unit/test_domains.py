from uuid import UUID
from datetime import datetime
import pytest
from app.domains import PartDomain, TestDomain


class TestTestDomain:
    """
    Test suite for the TestDomain entity.
    """

    @pytest.fixture(autouse=True)
    def _setup_domain(self):
        """
        Set up a TestDomain instance with predefined
        values for testing purposes.
        """
        self._domain = TestDomain(
            UUID("00000000-0000-0000-0000-000000000000"),
            UUID("00000000-0000-0000-0000-000000000001"),
            datetime(2021, 1, 1),
            True,
            {"name": "template_api", "type": "1"},
        )

    def test_constructor(self):
        """
        Test the constructor of the Domain class.
        """
        assert self._domain.id == UUID("00000000-0000-0000-0000-000000000000")
        assert self._domain.part_id == UUID(
            "00000000-0000-0000-0000-000000000001"
        )
        assert self._domain.timestamp == datetime(2021, 1, 1)
        assert self._domain.successful is True
        assert self._domain.data == {"name": "template_api", "type": "1"}

    def test_set_data(self):
        """
        Test the set_data method of the Domain class.
        """
        self._domain.set_data(
            {"name": "template_api", "type": "3", "note": "test version"}
        )
        assert self._domain.data == {
            "name": "template_api",
            "type": "3",
            "note": "test version",
        }

    def test_set_successful(self):
        """
        Test the set_successful method of the Domain class.
        """
        self._domain.set_success_state(False)
        assert self._domain.successful is False

    def test_set_timestamp(self):
        """
        Test the set_timestamp method of the Domain class.
        """
        self._domain.set_timestamp(datetime(2022, 1, 2))
        assert self._domain.timestamp == datetime(2022, 1, 2)

    def test_to_dict(self):
        """
        Test the to_dict method of the Domain class.
        """
        assert self._domain.to_dict() == {
            "id": "00000000-0000-0000-0000-000000000000",
            "part_id": "00000000-0000-0000-0000-000000000001",
            "timestamp": str(datetime(2021, 1, 1)),
            "successful": True,
            "data": {"name": "template_api", "type": "1"},
        }

    def test_str(self):
        """
        Test the __str__ method of the Domain class.
        """
        assert str(self._domain) == (
            "id=00000000-0000-0000-0000-000000000000, "
            "part_id=00000000-0000-0000-0000-000000000001, "
            "timestamp=2021-01-01 00:00:00, successful=True, "
            "data={'name': 'template_api', 'type': '1'}"
        )

    def test_repr(self):
        """
        Test the __repr__ method of the Domain class.
        """
        assert repr(self._domain) == (
            "TestDomain(id=UUID('00000000-0000-0000-0000-000000000000'), "
            "part_id=UUID('00000000-0000-0000-0000-000000000001'), "
            "timestamp=datetime.datetime(2021, 1, 1, 0, 0), successful=True, "
            "data={'name': 'template_api', 'type': '1'})"
        )

    def test_eq(self):
        """
        Test the __eq__ method of the Domain class.
        """
        assert self._domain == TestDomain(
            id=UUID("00000000-0000-0000-0000-000000000000"),
            part_id=UUID("00000000-0000-0000-0000-000000000001"),
            timestamp=datetime(2021, 1, 1),
            successful=True,
            data={"name": "template_api", "type": "1"},
        )


class TestPartDomain:
    """
    Test suite for the TestDomain entity.
    """

    @pytest.fixture(autouse=True)
    def _setup_domain(self):
        """
        Set up a TestDomain instance with predefined values
        for testing purposes.
        """
        self._domain = PartDomain(
            UUID("00000000-0000-0000-0000-000000000000"),
            "part_1",
            datetime(2021, 1, 1),
        )

    def test_constructor(self):
        """
        Test the constructor of the Domain class.
        """
        assert self._domain.name == "part_1"
        assert self._domain.id == UUID("00000000-0000-0000-0000-000000000000")
        assert self._domain.modified_timestamp == datetime(2021, 1, 1)

    def test_set_modified_timestamp(self):
        """
        Test the set_modified_timestamp method of the Domain class.
        """
        self._domain.set_modified_timestamp(datetime(2021, 1, 2))
        assert self._domain.modified_timestamp == datetime(2021, 1, 2)

    def test_to_dict(self):
        """
        Test the to_dict method of the Domain class.
        """
        assert self._domain.to_dict() == {
            "id": "00000000-0000-0000-0000-000000000000",
            "name": "part_1",
            "modified_timestamp": str(datetime(2021, 1, 1)),
        }

    def test_str(self):
        """
        Test the __str__ method of the Domain class.
        """
        assert str(self._domain) == (
            "id=00000000-0000-0000-0000-000000000000, "
            "name=part_1, "
            "modified_timestamp=2021-01-01 00:00:00"
        )

    def test_repr(self):
        """
        Test the __repr__ method of the Domain class.
        """
        assert repr(self._domain) == (
            "PartDomain(id=UUID('00000000-0000-0000-0000-000000000000'), "
            "name='part_1', "
            "modified_timestamp=datetime.datetime(2021, 1, 1, 0, 0))"
        )

    def test_eq(self):
        """
        Test the __eq__ method of the Domain class.
        """
        assert self._domain == PartDomain(
            id=UUID("00000000-0000-0000-0000-000000000000"),
            name="part_1",
            modified_timestamp=datetime(2021, 1, 1),
        )
