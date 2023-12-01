from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi_class import View

from app.exceptions import NoPartFound
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

router = APIRouter()


@router.get("/", summary="Root", description="Root")
async def get_root() -> str:
    return "Welcome to the template api !!"


@View(router, path="/parts")
class PartView:
    async def get(
        self,
        service: ServiceShowPart = Depends(ServiceShowPart),
        limit: int = 10,
        skip: int = 0,
    ) -> JSONResponse:
        """
        Retrieve all parts from the database.

        Args:
           service (ServiceShowPart): The service to use for retrieving parts.
           limit (int): The maximum number of parts to retrieve.
           skip (int): The number of parts to skip.
        Returns:
            JSONResponse: A JSON response containing the serialized parts data.
        """
        parts = await service.show_parts(limit, skip)
        content = [part.to_dict() for part in parts]
        return JSONResponse(content=content, status_code=200)

    async def post(
        self,
        part_dto: PartRegistrationDTO,
        service: ServiceCreatePart = Depends(ServiceCreatePart),
    ) -> JSONResponse:
        """
        Create a new part.

        Args:
            part_dto (PartRegistrationDTO):
                The DTO containing the part data.
            service (ServiceCreatePart):
                The service used to create the part.
                Defaults to ServiceCreatePart.

        Returns:
            JSONResponse:
                The serialized content of the created part and a 201 status code.
        """
        part = await service.create_part(part_dto)
        content = part.to_dict()
        response = JSONResponse(content=content, status_code=201)
        return response

    async def delete(
        self,
        id: UUID,
        service: ServiceDeletePart = Depends(ServiceDeletePart),
    ) -> JSONResponse:
        """
        Deletes a part with the given ID.

        Args:
            id (UUID):
                The ID of the part to delete.
            service (ServiceDeletePart, optional):
                The service to use for deleting the part.
                Defaults to ServiceDeletePart.

        Returns:
            JSONResponse:
                A JSON response indicating whether the part was deleted successfully.
        """
        await service.delete_part(id)
        content = {"message": "Part deleted successfully"}
        return JSONResponse(content=content, status_code=200)


@View(router, path="/tests")
class TestView:
    async def get(
        self,
        service: ServiceShowTest = Depends(ServiceShowTest),
        limit: int = 10,
        skip: int = 0,
    ) -> JSONResponse:
        """
        Retrieve a list of tests.

        Args:
            service (ServiceShowTest): An instance of ServiceShowTest.
            limit (int): The maximum number of tests to retrieve.
            skip (int): The number of tests to skip.

        Returns:
            JSONResponse: A JSON response containing the serialized content of the retrieved tests.
        """
        data = await service.show_tests(limit, skip)
        content = [test.to_dict() for test in data]
        return JSONResponse(content=content, status_code=200)

    async def post(
        self,
        part_dto: TestRegistrationDTO,
        service: ServiceCreateTest = Depends(ServiceCreateTest),
    ) -> JSONResponse:
        """
        Create a new test.

        Args:
            part_dto (TestRegistrationDTO):
                The test registration data.
            service (ServiceCreateTest):
                The service used to create the test.

        Returns:
            JSONResponse:
                The serialized test data with a 201 status code.
        """
        try:
            test = await service.create_test(part_dto)
            content = test.to_dict()
            response = JSONResponse(content=content, status_code=201)
        except NoPartFound:
            response = JSONResponse(
                content={"Message": "Part not found"}, status_code=404
            )
        return response

    async def patch(
        self,
        test_dto: TestUpdateDTO,
        service: ServiceUpdateTest = Depends(ServiceUpdateTest),
    ) -> JSONResponse:
        """
        Update a test resource.

        Args:
            test_dto (TestUpdateDTO): The DTO containing the updated test data.
            service (ServiceUpdateTest): The service used to update the test data.

        Returns:
            JSONResponse: The JSON response containing the updated test data.
        """

        test = await service.update_data(test_dto)
        content = test.to_dict()
        return JSONResponse(content=content, status_code=200)

    async def delete(
        self,
        id: UUID,
        service: ServiceDeleteTest = Depends(ServiceDeleteTest),
    ) -> JSONResponse:
        """
        Deletes a test with the given ID.

        Args:
            id (UUID):
                The ID of the test to delete.
            service (ServiceDeleteTest):
                The service to use for deleting the test.
                Defaults to ServiceDeleteTest.

        Returns:
            JSONResponse: A JSON response indicating whether the test was deleted successfully.
        """
        await service.delete_test(id)
        serialized_content = {"message": "Test deleted successfully"}
        return JSONResponse(content=serialized_content, status_code=200)
