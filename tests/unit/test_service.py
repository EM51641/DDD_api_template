from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID
import pytest
import pytest_asyncio
from app.domains import PartDomain, TestDomain
from app.repository import PartRepository, TestRepository
from app.schemas import PartRegistrationDTO, TestRegistrationDTO, TestUpdateDTO
from app.service import (
    ServiceCreatePart,
    ServiceCreateTest,
    ServiceDeletePart,
    ServiceDeleteTest,
    ServiceShowPart,
    ServiceShowTest,
    ServiceUpdateTest,
)
from app.unit_of_work import TestUnitOfWork
from typing import Any


class BaseTestService:
    @pytest.fixture(autouse=True)
    def _patch_uuid4(self):
        with patch(
            "app.service.uuid4",
            return_value=UUID("12345678123456781234567812345678"),
        ):
            yield

    @pytest.fixture(autouse=True)
    def _patch_datetime(self):
        with patch("app.service.datetime") as _mock:
            _mock.utcnow.return_value = datetime(2020, 1, 1)
            yield

    @pytest.fixture(autouse=True)
    def _setup_unit_of_work(self):
        self._unit_of_work = Mock(
            TestUnitOfWork,
            test_repository=AsyncMock(TestRepository),
            part_repository=AsyncMock(PartRepository),
        )


class TestServiceCreatePart(BaseTestService):
    @pytest.fixture(autouse=True)
    def _setup_service(self, _setup_unit_of_work):
        self._service = ServiceCreatePart(self._unit_of_work)

    @pytest.mark.asyncio
    async def test_create_part(self):
        """
        Test case for the create_part method of the PartService class.

        It tests that the method creates a new part with the given name and returns it with the correct attributes.
        """
        dto = Mock(PartRegistrationDTO)
        dto.name = "part_201"

        part = await self._service.create_part(dto)

        self._unit_of_work.part_repository.add.assert_called_once_with(
            PartDomain(
                id=UUID("12345678123456781234567812345678"),
                name="part_201",
                modified_timestamp=datetime(2020, 1, 1),
            )
        )
        self._unit_of_work.save.assert_called_once()

        assert part.id == UUID("12345678123456781234567812345678")
        assert part.name == "part_201"
        assert part.modified_timestamp == datetime(2020, 1, 1)


class TestServiceCreateTest(BaseTestService):
    @pytest.fixture(autouse=True)
    def _setup_service(self, _setup_unit_of_work):
        self._service = ServiceCreateTest(self._unit_of_work)

    @pytest.mark.asyncio
    async def test_create_part(self):
        """
        Test the create_test method of the service with a mock DTO.
        Assert that the test is added to the repository and saved correctly,
        and that the returned test object has the expected properties.
        """
        dto = Mock(
            TestRegistrationDTO,
            part_id=UUID("12345678123456781234567822345678"),
            successful=False,
            data={"test": "data"},
        )

        test = await self._service.create_test(dto)

        self._unit_of_work.test_repository.add.assert_called_once_with(
            TestDomain(
                id=UUID("12345678123456781234567812345678"),
                part_id=UUID("12345678123456781234567822345678"),
                timestamp=datetime(2020, 1, 1),
                successful=False,
                data={"test": "data"},
            )
        )
        self._unit_of_work.save.assert_called_once()

        assert test.id == UUID("12345678123456781234567812345678")
        assert test.part_id == UUID("12345678123456781234567822345678")
        assert test.timestamp == datetime(2020, 1, 1)
        assert test.successful is False
        assert test.data == {"test": "data"}


class TestServiceShowPart(BaseTestService):
    @pytest.fixture(autouse=True)
    def _setup_service(self, _setup_unit_of_work):
        """
        Sets up the service and unit of work for testing.
        """
        self._service = ServiceShowPart(self._unit_of_work)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "limit, offset", [(10, 3), (20, 10), (23, 24), (24, 13)]
    )
    async def test_show_parts(self, limit: int, offset: int) -> None:
        """
        Test case for the `show_parts` method of the `Service` class.

        This test ensures that the `show_parts` method returns the expected number of parts
        when called with the specified `limit` and `offset` parameters. It also checks that
        the `find_all` method of the part repository is called with the correct parameters.

        Args:
            limit (int): The maximum number of parts to return.
            offset (int): The offset from which to start returning parts.

        Returns:
            None
        """
        self._unit_of_work.part_repository.find_all.return_value = limit * [
            Mock(PartDomain)
        ]

        parts = await self._service.show_parts(limit, offset)
        self._unit_of_work.part_repository.find_all.assert_called_once_with(
            limit=limit, offset=offset
        )

        assert len(parts) == limit


class TestServiceShowTest(BaseTestService):
    @pytest.fixture(autouse=True)
    def _setup_service(self, _setup_unit_of_work):
        """
        Set up the service by creating a mock unit of work and initializing the service with it.
        """
        self._service = ServiceShowTest(self._unit_of_work)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("limit, offset", [(1, 0), (2, 1), (3, 2), (4, 3)])
    async def test_show_tests(self, limit: int, offset: int) -> None:
        """
        Test that the show_tests method of the service returns the expected number of tests
        and calls the find_all method of the test repository with the correct arguments.
        """
        self._unit_of_work.test_repository.find_all.return_value = limit * [
            Mock(TestDomain)
        ]

        tests = await self._service.show_tests(limit, offset)

        self._unit_of_work.test_repository.find_all.assert_called_once_with(
            limit=limit, offset=offset
        )
        assert len(tests) == limit


class TestServiceDeletePart(BaseTestService):
    @pytest.fixture(autouse=True)
    def _setup_service(self, _setup_unit_of_work):
        """
        Set up the service by creating a mock unit of work and initializing the service with it.
        """
        self._service = ServiceDeletePart(self._unit_of_work)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "id",
        [
            UUID("12345678123456781234567812345678"),
            UUID("87654321876543218765432187654321"),
        ],
    )
    async def test_delete_part(self, id: UUID):
        """
        Test that the delete_part method of the service calls the delete method of the part repository
        with the correct arguments.
        """
        part = Mock(PartDomain)
        self._unit_of_work.part_repository.find_by_id.return_value = part

        await self._service.delete_part(id)

        self._unit_of_work.part_repository.find_by_id.assert_called_once_with(
            id
        )
        self._unit_of_work.part_repository.remove.assert_called_once_with(part)
        self._unit_of_work.save.assert_called_once()


class TestServiceDeleteTest(BaseTestService):
    @pytest.fixture(autouse=True)
    def _setup_service(self, _setup_unit_of_work):
        """
        Set up the service by creating a mock unit of work and initializing the service with it.
        """
        self._service = ServiceDeleteTest(self._unit_of_work)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "id",
        [
            UUID("32345678123456781234567812345678"),
            UUID("47654321876543218765432187654321"),
        ],
    )
    async def test_delete_test(self, id: UUID):
        """
        Test that the delete_test method of the service calls the delete method of the test repository
        with the correct arguments.
        """
        test = Mock(TestDomain)
        self._unit_of_work.test_repository.find_by_id.return_value = test

        await self._service.delete_test(id)

        self._unit_of_work.test_repository.find_by_id.assert_called_once_with(
            id
        )
        self._unit_of_work.test_repository.remove.assert_called_once_with(test)
        self._unit_of_work.save.assert_called_once()


class TestServiceUpdateTest(BaseTestService):
    @pytest.fixture(autouse=True)
    def _setup_service(self, _setup_unit_of_work):
        """
        Set up the service by creating a mock unit of work
        and initializing the service with it.
        """
        self._service = ServiceUpdateTest(self._unit_of_work)

    @pytest.fixture
    def _setup_test(self, _setup_unit_of_work):
        """
        Set up a test domain
        """
        self._test = TestDomain(
            id=UUID("47654321876543218765432187654321"),
            part_id=UUID("47654321876543218765432187654323"),
            timestamp=datetime(2021, 1, 1),
            successful=True,
            data={"type": "standard", "name": "test"},
        )

    @pytest.fixture
    def _setup_dto(self, _setup_unit_of_work):
        """
        Set up a test domain
        """
        self._dto = Mock(
            TestUpdateDTO,
            id=UUID("47654321876543218765432187654321"),
            successful=None,
            timestamp=None,
            data={"type": "titan", "name": "test"},
        )

    @pytest_asyncio.fixture
    async def _setup_update_data(self, _setup_test, _setup_dto):
        self._unit_of_work.test_repository.find_by_id.return_value = self._test
        self._updated_test = await self._service.update_data(self._dto)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "domain, dto, timestamp, success, data",
        [
            (
                TestDomain(
                    id=UUID("47654321876543218765432187654321"),
                    part_id=UUID("47654321876543218765432187654323"),
                    timestamp=datetime(2019, 1, 1),
                    successful=True,
                    data={"type": "standard", "name": "test"},
                ),
                Mock(
                    TestUpdateDTO,
                    id=UUID("47654321876543218765432187654321"),
                    successful=None,
                    timestamp=None,
                    data={"type": "titan", "name": "test"},
                ),
                datetime(2019, 1, 1),
                True,
                {"type": "titan", "name": "test"},
            ),
            (
                TestDomain(
                    id=UUID("47654321876543218765432187654321"),
                    part_id=UUID("47654321876543218765432187654323"),
                    timestamp=datetime(2022, 1, 1),
                    successful=False,
                    data={"type": "standard", "name": "test"},
                ),
                Mock(
                    TestUpdateDTO,
                    id=UUID("47654321876543218765432187654321"),
                    successful=True,
                    timestamp=datetime(2021, 1, 1),
                    data=None,
                ),
                datetime(2021, 1, 1),
                True,
                {"type": "standard", "name": "test"},
            ),
        ],
    )
    async def test_update_data(
        self,
        domain: TestDomain,
        dto: TestUpdateDTO,
        timestamp: datetime | None,
        success: bool | None,
        data: dict[Any, Any] | None,
    ):
        """
        Test that the delete_test method of the service calls the delete method of the test repository
        with the correct arguments.
        """
        self._unit_of_work.test_repository.find_by_id.return_value = domain
        test = await self._service.update_data(dto)

        assert test.id == UUID("47654321876543218765432187654321")
        assert test.part_id == UUID("47654321876543218765432187654323")
        assert test.timestamp == timestamp
        assert test.successful is success
        assert test.data == data

    async def test_update_data_side_effects_repository_called(
        self, _setup_update_data
    ):
        """
        Test side effects while updating data.
        """

        self._unit_of_work.test_repository.find_by_id.assert_called_once_with(
            UUID("47654321876543218765432187654321")
        )

    async def test_update_data_side_effects_modify_called(
        self, _setup_update_data
    ):
        self._unit_of_work.test_repository.modify.assert_called_once_with(
            self._updated_test
        )

    async def test_update_data_side_effects_persistance_called(
        self, _setup_update_data
    ):
        self._unit_of_work.save.assert_called_once()
