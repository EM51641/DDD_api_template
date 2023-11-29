from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, TypeVar
from uuid import UUID, uuid4
from fastapi import Depends
from app.domains import PartDomain, TestDomain
from app.exceptions import NoEntityFoundError, NoPartFound
from app.schemas import (
    PartRegistrationDTO,
    TestUpdateDTO,
    TestRegistrationDTO,
)
from app.unit_of_work import BaseUnitOfWork, TestUnitOfWork

TUnitOfWork = TypeVar("TUnitOfWork", bound=BaseUnitOfWork)


class BaseService(ABC, Generic[TUnitOfWork]):
    def __init__(self, unit_of_work: TUnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    @property
    def unit_of_work(self) -> TUnitOfWork:
        return self._unit_of_work


class BaseServiceCreatePart(BaseService[TestUnitOfWork]):
    def __init__(
        self, unit_of_work: TestUnitOfWork = Depends(TestUnitOfWork)
    ) -> None:
        """
        Initializes an instance of MyClass.

        Args:
            unit_of_work (TestUnitOfWork):
                An instance of TestUnitOfWork. Defaults to Depends(TestUnitOfWork).
        """
        super().__init__(unit_of_work)

    @abstractmethod
    async def create_part(self, part_dto: PartRegistrationDTO) -> PartDomain:
        """Not implemented yet"""


class ServiceCreatePart(BaseServiceCreatePart):
    def __init__(
        self, unit_of_work: TestUnitOfWork = Depends(TestUnitOfWork)
    ) -> None:
        """
        Initializes an instance of MyClass.

        Args:
            unit_of_work (TestUnitOfWork):
                An instance of TestUnitOfWork. Defaults to Depends(TestUnitOfWork).
        """
        super().__init__(unit_of_work)

    async def create_part(self, part_dto: PartRegistrationDTO) -> PartDomain:
        """
        Creates a new part using the provided PartRegistrationDTO and adds it to the part repository.

        Args:
            part_dto (PartRegistrationDTO):
                The DTO containing the information needed to create the new part.

        Returns:
            None
        """
        part = self._generate_part(part_dto)
        self._unit_of_work.part_repository.add(part)
        await self._unit_of_work.save()
        return part

    def _generate_part(self, part_dto: PartRegistrationDTO) -> PartDomain:
        """
        Generates a new PartDomain object based on the provided PartRegistrationDTO.

        Args:
            part_dto (PartRegistrationDTO):
                The DTO containing the data for the new part.

        Returns:
            PartDomain: The newly generated PartDomain object.
        """
        return PartDomain(
            id=uuid4(),
            name=part_dto.name,
            modified_timestamp=datetime.utcnow(),
        )


class BaseServiceCreateTest(BaseService[TestUnitOfWork]):
    def __init__(
        self, unit_of_work: TestUnitOfWork = Depends(TestUnitOfWork)
    ) -> None:
        """
        Initializes an instance of MyClass.

        Args:
            unit_of_work (TestUnitOfWork):
                An instance of TestUnitOfWork. Defaults to Depends(TestUnitOfWork).
        """
        super().__init__(unit_of_work)

    @abstractmethod
    async def create_test(self, test_dto: TestRegistrationDTO) -> TestDomain:
        """Not implemented yet"""


class ServiceCreateTest(BaseServiceCreateTest):
    async def create_test(self, test_dto: TestRegistrationDTO) -> TestDomain:
        """
        Creates a new test using the provided TestRegistrationDTO.

        Args:
            test_dto (TestRegistrationDTO):
                The DTO containing the information for the new test.

        Returns:
            None
        """
        await self._validate_part_id(test_dto.part_id)
        test = self._generate_test(test_dto)
        self._unit_of_work.test_repository.add(test)
        await self._unit_of_work.save()
        return test

    async def _validate_part_id(self, part_id: UUID) -> None:
        """
        Validates that the provided part_id exists in the database.

        Args:
            part_id (uuid4): The part_id to validate.

        Returns:
            bool: True if the part_id exists, False otherwise.
        """
        try:
            await self._unit_of_work.part_repository.find_by_id(part_id)
        except NoEntityFoundError:
            raise NoPartFound()

    def _generate_test(self, test_dto: TestRegistrationDTO) -> TestDomain:
        """
        Generates a TestDomain object based on the provided TestRegistrationDTO.

        Args:
            test_dto (TestRegistrationDTO): The TestRegistrationDTO object to generate the TestDomain from.

        Returns:
            TestDomain: The generated TestDomain object.
        """
        return TestDomain(
            id=uuid4(),
            part_id=test_dto.part_id,
            timestamp=datetime.utcnow(),
            successful=test_dto.successful,
            data=test_dto.data,
        )


class BaseServiceShowPart(BaseService[TestUnitOfWork]):
    def __init__(
        self, unit_of_work: TestUnitOfWork = Depends(TestUnitOfWork)
    ) -> None:
        """
        Initializes an instance of MyClass.

        Args:
            unit_of_work (TestUnitOfWork, optional): An instance of TestUnitOfWork. Defaults to Depends(TestUnitOfWork).
        """
        super().__init__(unit_of_work)

    @abstractmethod
    async def show_parts(self, limit: int, offset: int) -> list[PartDomain]:
        """Not implemented yet"""


class ServiceShowPart(BaseServiceShowPart):
    async def show_parts(self, limit: int, offset: int) -> list[PartDomain]:
        """
        Retrieves all PartDomain objects

        Returns:
            list[PartDomain]:
                The retrieved PartDomain object.
        """

        list_parts = await self._unit_of_work.part_repository.find_all(
            limit=limit, offset=offset
        )
        return list_parts


class BaseServiceShowTest(BaseService[TestUnitOfWork]):
    def __init__(
        self, unit_of_work: TestUnitOfWork = Depends(TestUnitOfWork)
    ) -> None:
        """
        Initializes an instance of MyClass.

        Args:
            unit_of_work (TestUnitOfWork, optional):
                An instance of TestUnitOfWork. Defaults to Depends(TestUnitOfWork).
        """
        super().__init__(unit_of_work)

    @abstractmethod
    async def show_tests(self, limit: int, offset: int) -> list[TestDomain]:
        """Not implemented yet"""


class ServiceShowTest(BaseServiceShowTest):
    async def show_tests(self, limit: int, offset: int) -> list[TestDomain]:
        """
        Retrieves all TestDomain objects

        Returns:
            list[TestDomain]:
                The retrieved TestDomain object.
        """

        list_tests = await self._unit_of_work.test_repository.find_all(
            limit=limit, offset=offset
        )
        return list_tests


class BaseServiceDeletePart(BaseService[TestUnitOfWork]):
    def __init__(
        self, unit_of_work: TestUnitOfWork = Depends(TestUnitOfWork)
    ) -> None:
        """
        Initializes an instance of MyClass.

        Args:
            unit_of_work (TestUnitOfWork, optional): An instance of TestUnitOfWork. Defaults to Depends(TestUnitOfWork).
        """
        super().__init__(unit_of_work)

    @abstractmethod
    async def delete_part(self, id: UUID) -> None:
        """Not implemented yet"""


class ServiceDeletePart(BaseServiceDeletePart):
    async def delete_part(self, id: UUID) -> None:
        """
        Deletes a part using the provided id.

        Args:
            id (UUID):
                The id of the part to be deleted.

        Returns:
            None
        """
        part = await self._unit_of_work.part_repository.find_by_id(id)
        await self._unit_of_work.part_repository.remove(part)
        await self._unit_of_work.save()


class BaseServiceDeleteTest(BaseService[TestUnitOfWork]):
    def __init__(
        self, unit_of_work: TestUnitOfWork = Depends(TestUnitOfWork)
    ) -> None:
        """
        Initializes an instance of MyClass.

        Args:
            unit_of_work (TestUnitOfWork, optional): An instance of TestUnitOfWork. Defaults to Depends(TestUnitOfWork).
        """
        super().__init__(unit_of_work)

    @abstractmethod
    async def delete_test(self, id: UUID) -> None:
        """Not implemented yet"""


class ServiceDeleteTest(BaseServiceDeleteTest):
    async def delete_test(self, id: UUID) -> None:
        """
        Deletes a test using the provided id.

        Args:
            id (UUID):
                The id of the test to be deleted.

        Returns:
            None
        """
        test = await self._unit_of_work.test_repository.find_by_id(id)
        await self._unit_of_work.test_repository.remove(test)
        await self._unit_of_work.save()


class BaseServiceChangeTest(BaseService[TestUnitOfWork]):
    def __init__(
        self, unit_of_work: TestUnitOfWork = Depends(TestUnitOfWork)
    ) -> None:
        """
        Initializes an instance of MyClass.

        Args:
            unit_of_work (TestUnitOfWork, optional): An instance of TestUnitOfWork. Defaults to Depends(TestUnitOfWork).
        """
        super().__init__(unit_of_work)

    @abstractmethod
    async def update_data(self, dto: TestUpdateDTO) -> TestDomain:
        """Not implemented yet"""


class ServiceUpdateTest(BaseServiceChangeTest):
    """
    Service class for updating a test.
    """

    async def update_data(self, dto: TestUpdateDTO) -> TestDomain:
        """
        Updates a test using the provided TestUpdateDTO.

        Args:
            dto (TestUpdateDTO):
                The DTO containing the information for the test update.

        Returns:
            None
        """
        test = await self._get_test(dto)
        await self._update_data(test, dto)
        await self._save(test)
        return test

    async def _update_data(self, test: TestDomain, dto: TestUpdateDTO) -> None:
        """
        Update the data for a given test using the provided DTO.

        Args:
            test: The test object to update.
            dto: The DTO containing the updated data.

        Returns:
            None
        """
        await self._update_extra(test, dto)
        await self._update_state(test, dto)
        await self._update_timestamp(test, dto)

    async def _save(self, test: TestDomain) -> None:
        """
        Saves the given TestDomain object by modifying it in the test repository and saving the changes.

        Args:
            test (TestDomain): The TestDomain object to be saved.

        Returns:
            None
        """
        await self._unit_of_work.test_repository.modify(test)
        await self._unit_of_work.save()

    async def _update_extra(
        self, test: TestDomain, dto: TestUpdateDTO
    ) -> None:
        """
        Update the extra information of a test.

        Args:
            test (TestDomain): The test domain object to update.
            dto (TestUpdateDTO): The DTO containing the updated data.

        Returns:
            None
        """
        if dto.data:
            test.set_data(dto.data)

    async def _update_state(
        self, test: TestDomain, dto: TestUpdateDTO
    ) -> None:
        """
        Update the state of the test based on the provided DTO.

        Args:
            test (TestDomain): The test domain object to update.
            dto (TestUpdateDTO): The DTO containing the updated information.

        Returns:
            None
        """
        if dto.successful:
            test.set_success_state(dto.successful)

    async def _update_timestamp(
        self, test: TestDomain, dto: TestUpdateDTO
    ) -> None:
        """
        Update the timestamp of a test.

        Args:
            test (TestDomain): The test domain object.
            dto (TestUpdateDTO): The DTO containing the updated timestamp.

        Returns:
            None
        """
        if dto.timestamp:
            test.set_timestamp(dto.timestamp)

    async def _get_test(
        self,
        dto: TestUpdateDTO,
    ) -> TestDomain:
        """
        Retrieves a test using the provided id.

        Args:
            id (UUID):
                The id of the test to be retrieved.

        Returns:
            TestDomain
        """
        test = await self._unit_of_work.test_repository.find_by_id(dto.id)
        return test
