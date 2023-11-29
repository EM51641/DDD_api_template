import pytest_asyncio
import pytest
from unittest.mock import MagicMock
from uuid import UUID
import datetime
from fastapi import FastAPI
from httpx import AsyncClient
from app.domains import PartDomain, TestDomain
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import NoPartFound
from app.service import (
    ServiceCreatePart,
    ServiceCreateTest,
    ServiceDeletePart,
    ServiceDeleteTest,
    ServiceShowPart,
    ServiceShowTest,
    ServiceUpdateTest,
)


class BaseIntegrationTestEndpoint:
    @pytest.fixture(autouse=True)
    def setup_client(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        self._client = client
        self._session = db_session


class TestPartList(BaseIntegrationTestEndpoint):
    @pytest.fixture(autouse=True)
    def _patch_services(self, app: FastAPI):
        self._service_list_mock = MagicMock(ServiceShowPart)
        app.dependency_overrides[
            ServiceShowPart
        ] = lambda: self._service_list_mock

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "query_string,limit,offset,parts",
        [
            (
                "",
                10,
                0,
                [
                    PartDomain(
                        id=UUID("e3e70682-c209-4cac-629f-6fbed82c07cd"),
                        name="Part 53",
                        modified_timestamp=datetime.datetime(
                            2010, 5, 17, 15, 25, 58
                        ),
                    ),
                    PartDomain(
                        id=UUID("f7c1bd87-4da5-e709-d471-3d60c8a70639"),
                        name="Part 61",
                        modified_timestamp=datetime.datetime(
                            2015, 10, 7, 16, 8, 18
                        ),
                    ),
                    PartDomain(
                        id=UUID("9e4d6e3c-1846-d424-c17c-627923c6612f"),
                        name="Part 32",
                        modified_timestamp=datetime.datetime(
                            2018, 12, 26, 19, 57, 9
                        ),
                    ),
                    PartDomain(
                        id=UUID("12e0c8b2-bad6-40fb-1948-8dec4f65d4d9"),
                        name="Part 87",
                        modified_timestamp=datetime.datetime(
                            2015, 8, 18, 3, 22, 27
                        ),
                    ),
                    PartDomain(
                        id=UUID("e9bb17bc-a3f2-c9bf-9c63-16b950f24455"),
                        name="Part 26",
                        modified_timestamp=datetime.datetime(
                            2018, 8, 15, 16, 16, 3
                        ),
                    ),
                    PartDomain(
                        id=UUID("ea7e9d49-8c77-8ea6-eb20-83e6ce164dba"),
                        name="Part 1",
                        modified_timestamp=datetime.datetime(
                            2011, 12, 27, 12, 45, 52
                        ),
                    ),
                    PartDomain(
                        id=UUID("004ae545-a011-6be5-ab0c-1681c8f8e3d0"),
                        name="Part 78",
                        modified_timestamp=datetime.datetime(
                            2017, 6, 8, 23, 20, 45
                        ),
                    ),
                    PartDomain(
                        id=UUID("eac1c14f-30e9-c5cc-101f-bcccded733e8"),
                        name="Part 72",
                        modified_timestamp=datetime.datetime(
                            2013, 4, 26, 4, 51, 34
                        ),
                    ),
                    PartDomain(
                        id=UUID("fe43c49e-1498-18d1-1759-edc372ae2244"),
                        name="Part 40",
                        modified_timestamp=datetime.datetime(
                            2018, 8, 4, 9, 35, 18
                        ),
                    ),
                    PartDomain(
                        id=UUID("552f233a-8c25-166a-1ff3-9849b4e1357d"),
                        name="Part 69",
                        modified_timestamp=datetime.datetime(
                            2013, 10, 18, 18, 18, 28
                        ),
                    ),
                ],
            ),
            (
                "limit=5&skip=5",
                5,
                5,
                [
                    PartDomain(
                        id=UUID("5b7c709a-cb17-5a5a-fb82-860deabca8d0"),
                        name="Part 10",
                        modified_timestamp=datetime.datetime(
                            2015, 10, 4, 15, 37, 40
                        ),
                    ),
                    PartDomain(
                        id=UUID("3e37952d-30bc-ab0e-d857-010255d44936"),
                        name="Part 2",
                        modified_timestamp=datetime.datetime(
                            2021, 5, 4, 22, 14, 23
                        ),
                    ),
                    PartDomain(
                        id=UUID("6d16ee18-5521-16dd-2ba4-b180cb69ca38"),
                        name="Part 7",
                        modified_timestamp=datetime.datetime(
                            2011, 3, 28, 22, 14, 2
                        ),
                    ),
                    PartDomain(
                        id=UUID("e8f6cf32-a25b-59fd-92e8-e269d12ecbc4"),
                        name="Part 68",
                        modified_timestamp=datetime.datetime(
                            2019, 11, 3, 0, 7, 40
                        ),
                    ),
                    PartDomain(
                        id=UUID("9371a71f-d480-865f-9b38-fe803042e325"),
                        name="Part 15",
                        modified_timestamp=datetime.datetime(
                            2016, 2, 12, 3, 2, 38
                        ),
                    ),
                ],
            ),
            (
                "limit=2&skip=8",
                2,
                8,
                [
                    PartDomain(
                        id=UUID("ec62b2c8-2648-ee38-e074-05eb215663ab"),
                        name="Part 4",
                        modified_timestamp=datetime.datetime(
                            2023, 2, 23, 17, 43, 25
                        ),
                    ),
                    PartDomain(
                        id=UUID("468ff53d-864a-7a50-b48d-73f1d67e55fd"),
                        name="Part 66",
                        modified_timestamp=datetime.datetime(
                            2022, 4, 28, 6, 57, 43
                        ),
                    ),
                ],
            ),
            (
                "limit=3&skip=3",
                3,
                3,
                [
                    PartDomain(
                        id=UUID("402d0baf-878b-9f6b-57a1-cb712975d279"),
                        name="Part 15",
                        modified_timestamp=datetime.datetime(
                            2019, 8, 22, 5, 0, 30
                        ),
                    ),
                    PartDomain(
                        id=UUID("91b15f5d-e66c-d36e-68ef-8f5fae68690a"),
                        name="Part 65",
                        modified_timestamp=datetime.datetime(
                            2014, 11, 12, 12, 53, 42
                        ),
                    ),
                    PartDomain(
                        id=UUID("b0d9c2aa-8f83-7ef7-2746-0f22403d1f83"),
                        name="Part 1",
                        modified_timestamp=datetime.datetime(
                            2017, 12, 3, 10, 47, 2
                        ),
                    ),
                ],
            ),
            (
                "limit=1&skip=9",
                1,
                9,
                [
                    PartDomain(
                        id=UUID("0063e42f-14aa-451c-a69c-fb85d432f8db"),
                        name="Part 76",
                        modified_timestamp=datetime.datetime(
                            2014, 12, 11, 5, 15, 14
                        ),
                    )
                ],
            ),
        ],
    )
    async def test_show_all_parts(
        self,
        query_string: str,
        limit: int,
        offset: int,
        parts: list[PartDomain],
    ):
        self._service_list_mock.show_parts.return_value = parts
        response = await self._client.get(f"/parts?{query_string}")

        assert response.status_code == 200
        assert response.json() == [part.to_dict() for part in parts]


class TestPartPost(BaseIntegrationTestEndpoint):
    @pytest.fixture(autouse=True)
    def _patch_services(self, app: FastAPI):
        self._service_post_mock = MagicMock(ServiceCreatePart)
        app.dependency_overrides[
            ServiceCreatePart
        ] = lambda: self._service_post_mock

    @pytest.mark.asyncio
    @pytest.mark.parametrize("name", ["part_1", "part_42", "part_32"])
    async def test_post(self, name: str):
        """
        Test the POST method of the PartsController by creating a new part
        and verifying that it was added to the database.
        """
        part = PartDomain(
            id=UUID("e3e70682-c209-4cac-629f-6fbed82c07cd"),
            name=name,
            modified_timestamp=datetime.datetime(2010, 5, 17, 15, 25, 58),
        )

        self._service_post_mock.create_part.return_value = part

        response = await self._client.post(
            "/parts",
            json={"name": name},
        )

        assert response.status_code == 201
        assert response.json() == part.to_dict()


class TestPartDelete(BaseIntegrationTestEndpoint):
    @pytest.fixture(autouse=True)
    def _patch_services(self, app: FastAPI):
        self._service_delete_mock = MagicMock(ServiceDeletePart)
        app.dependency_overrides[
            ServiceDeletePart
        ] = lambda: self._service_delete_mock

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "id",
        [
            UUID("e3e70682-c209-4cac-629f-6fbed82c07cd"),
            UUID("f7c1bd87-4da5-e709-d471-3d60c8a70639"),
            UUID("9e4d6e3c-1846-d424-c17c-627923c6612f"),
        ],
    )
    async def test_delete(self, id: UUID):
        """
        Test the DELETE method of the PartsController by creating a new part
        and verifying that it was added to the database.
        """
        response = await self._client.delete(
            f"/parts?id={id}",
        )

        assert response.status_code == 200
        assert response.json() == {"message": "Part deleted successfully"}
        self._service_delete_mock.delete_part.assert_called_once_with(id)


class TestTestList(BaseIntegrationTestEndpoint):
    @pytest.fixture(autouse=True)
    def _patch_services(self, app: FastAPI):
        self._service_list_mock = MagicMock(ServiceShowTest)
        app.dependency_overrides[
            ServiceShowTest
        ] = lambda: self._service_list_mock

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "query_string,limit,offset,tests",
        [
            (
                "",
                10,
                0,
                [
                    TestDomain(
                        id=UUID("e3e70682-c209-4cac-629f-6fbed82c07cd"),
                        part_id=UUID("7f411fed-1e70-e799-33a1-d1c2ad4ab155"),
                        timestamp=datetime.datetime(2014, 5, 11, 10, 23, 44),
                        successful=False,
                        data={"type": "height", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("e87a1613-e443-df78-9558-867f5ba91faf"),
                        part_id=UUID("b0d9c2aa-8f83-7ef7-2746-0f22403d1f83"),
                        timestamp=datetime.datetime(2018, 8, 18, 15, 5, 10),
                        successful=True,
                        data={"type": "height", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("9a164106-cf6a-659e-b486-2b21fb97d435"),
                        part_id=UUID("e8f6cf32-a25b-59fd-92e8-e269d12ecbc4"),
                        timestamp=datetime.datetime(2020, 4, 9, 3, 53, 44),
                        successful=False,
                        data={"type": "design", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("50f24455-6f25-e2a2-5a92-118719c78df4"),
                        part_id=UUID("afb918c8-6e5b-ac20-725c-2675ca9571e4"),
                        timestamp=datetime.datetime(2011, 7, 21, 17, 21, 46),
                        successful=False,
                        data={"type": "height", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("ea7e9d49-8c77-8ea6-eb20-83e6ce164dba"),
                        part_id=UUID("f7c1bd87-4da5-e709-d471-3d60c8a70639"),
                        timestamp=datetime.datetime(2015, 11, 24, 16, 1, 43),
                        successful=True,
                        data={"type": "design", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("b421eaeb-5340-97ca-baf3-897a3e70f16a"),
                        part_id=UUID("fe43c49e-1498-18d1-1759-edc372ae2244"),
                        timestamp=datetime.datetime(2018, 11, 10, 3, 49, 33),
                        successful=True,
                        data={"type": "design", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("e005b860-51ef-1922-fe43-c49e149818d1"),
                        part_id=UUID("dc2151e1-7e56-ac3d-10cc-8711552ae5ca"),
                        timestamp=datetime.datetime(2024, 1, 30, 16, 44, 26),
                        successful=False,
                        data={"type": "quality", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("8a5006c1-ec18-8efb-d080-e66e552f233a"),
                        part_id=UUID("91b15f5d-e66c-d36e-68ef-8f5fae68690a"),
                        timestamp=datetime.datetime(2015, 9, 17, 6, 31),
                        successful=False,
                        data={"type": "quality", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("935ddd72-5129-fb7c-6288-e1a5cc457821"),
                        part_id=UUID("0063e42f-14aa-451c-a69c-fb85d432f8db"),
                        timestamp=datetime.datetime(2014, 5, 8, 10, 28, 6),
                        successful=True,
                        data={"type": "quality", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("79fdef7c-4293-0b33-a81a-d477fb3675b8"),
                        part_id=UUID("fe43c49e-1498-18d1-1759-edc372ae2244"),
                        timestamp=datetime.datetime(2018, 9, 19, 7, 23, 26),
                        successful=True,
                        data={"type": "quality", "priority": "1"},
                    ),
                ],
            ),
            (
                "limit=5&skip=5",
                5,
                5,
                [
                    TestDomain(
                        id=UUID("b421eaeb-5340-97ca-baf3-897a3e70f16a"),
                        part_id=UUID("fe43c49e-1498-18d1-1759-edc372ae2244"),
                        timestamp=datetime.datetime(2018, 11, 10, 3, 49, 33),
                        successful=True,
                        data={"type": "design", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("e005b860-51ef-1922-fe43-c49e149818d1"),
                        part_id=UUID("dc2151e1-7e56-ac3d-10cc-8711552ae5ca"),
                        timestamp=datetime.datetime(2024, 1, 30, 16, 44, 26),
                        successful=False,
                        data={"type": "quality", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("8a5006c1-ec18-8efb-d080-e66e552f233a"),
                        part_id=UUID("91b15f5d-e66c-d36e-68ef-8f5fae68690a"),
                        timestamp=datetime.datetime(2015, 9, 17, 6, 31),
                        successful=False,
                        data={"type": "quality", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("935ddd72-5129-fb7c-6288-e1a5cc457821"),
                        part_id=UUID("0063e42f-14aa-451c-a69c-fb85d432f8db"),
                        timestamp=datetime.datetime(2014, 5, 8, 10, 28, 6),
                        successful=True,
                        data={"type": "quality", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("79fdef7c-4293-0b33-a81a-d477fb3675b8"),
                        part_id=UUID("fe43c49e-1498-18d1-1759-edc372ae2244"),
                        timestamp=datetime.datetime(2018, 9, 19, 7, 23, 26),
                        successful=True,
                        data={"type": "quality", "priority": "1"},
                    ),
                ],
            ),
            (
                "limit=2&skip=8",
                2,
                8,
                [
                    TestDomain(
                        id=UUID("935ddd72-5129-fb7c-6288-e1a5cc457821"),
                        part_id=UUID("0063e42f-14aa-451c-a69c-fb85d432f8db"),
                        timestamp=datetime.datetime(2014, 5, 8, 10, 28, 6),
                        successful=True,
                        data={"type": "quality", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("79fdef7c-4293-0b33-a81a-d477fb3675b8"),
                        part_id=UUID("fe43c49e-1498-18d1-1759-edc372ae2244"),
                        timestamp=datetime.datetime(2018, 9, 19, 7, 23, 26),
                        successful=True,
                        data={"type": "quality", "priority": "1"},
                    ),
                ],
            ),
            (
                "limit=3&skip=3",
                3,
                3,
                [
                    TestDomain(
                        id=UUID("d450fe4a-ec4f-217b-b306-d1a8e5eeac76"),
                        part_id=UUID("084fa819-052d-aad3-26c0-0984c734bb05"),
                        timestamp=datetime.datetime(2020, 3, 4, 23, 0, 29),
                        successful=False,
                        data={"type": "weight", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("d3447490-96fd-35d0-adf2-0806e5214606"),
                        part_id=UUID("7f411fed-1e70-e799-33a1-d1c2ad4ab155"),
                        timestamp=datetime.datetime(2015, 2, 11, 10, 19, 44),
                        successful=False,
                        data={"type": "quality", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("964a870c-7c87-9b74-1d87-8f9f9cdf5a86"),
                        part_id=UUID("d1aa6c5e-3b01-9fcb-f96d-4403d48c93f3"),
                        timestamp=datetime.datetime(2012, 3, 24, 12, 15, 14),
                        successful=False,
                        data={"type": "quality", "priority": "3"},
                    ),
                ],
            ),
            (
                "limit=1&skip=9",
                1,
                9,
                [
                    TestDomain(
                        id=UUID("275f275c-c3f3-f74d-d386-1b58194665d3"),
                        part_id=UUID("1d7173e5-5bc7-fdeb-3123-4efe6e648043"),
                        timestamp=datetime.datetime(2024, 3, 20, 7, 7, 52),
                        successful=False,
                        data={"type": "design", "priority": "1"},
                    )
                ],
            ),
        ],
    )
    async def test_show_all_parts(
        self,
        query_string: str,
        limit: int,
        offset: int,
        tests: list[PartDomain],
    ):
        self._service_list_mock.show_tests.return_value = tests
        response = await self._client.get(f"/tests?{query_string}")

        assert response.status_code == 200
        assert response.json() == [test.to_dict() for test in tests]


class TestTestPost(BaseIntegrationTestEndpoint):
    @pytest.fixture(autouse=True)
    def _patch_services(self, app: FastAPI):
        self._service_post_mock = MagicMock(ServiceCreateTest)
        app.dependency_overrides[
            ServiceCreateTest
        ] = lambda: self._service_post_mock

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "part_id, successful, data",
        [
            (
                UUID("e3e70682-c209-4cac-629f-6fbed82c07cd"),
                False,
                {"type": "height", "priority": "2"},
            ),
            (
                UUID("f7c1bd87-4da5-e709-d471-3d60c8a70639"),
                True,
                {"type": "height", "priority": "3"},
            ),
            (
                UUID("9e4d6e3c-1846-d424-c17c-627923c6612f"),
                False,
                {"type": "design", "priority": "3"},
            ),
        ],
    )
    async def test_post(self, part_id: UUID, successful: bool, data: dict):
        """
        Test the POST method of the PartsController by creating a new part
        and verifying that it was added to the database.
        """
        test = TestDomain(
            id=UUID("275f275c-c3f3-f74d-d386-1b58194665d3"),
            part_id=part_id,
            timestamp=datetime.datetime(2024, 3, 20, 7, 7, 52),
            successful=successful,
            data=data,
        )

        self._service_post_mock.create_test.return_value = test

        response = await self._client.post(
            "/tests",
            json={
                "part_id": str(part_id),
                "successful": successful,
                "data": data,
            },
        )
        assert response.status_code == 201
        assert response.json() == test.to_dict()

    async def test_post_failure(self):
        """
        Test the POST method of the PartsController by creating a new part
        and verifying that it was added to the database.
        """

        self._service_post_mock.create_test.side_effect = NoPartFound()

        response = await self._client.post(
            "/tests",
            json={
                "part_id": "275f275c-c3f3-f74d-d386-1b58194665d3",
                "successful": False,
                "data": {"type": "test"},
            },
        )

        assert response.status_code == 404
        assert response.json() == {"Message": "Part not found"}


class TestTestDelete(BaseIntegrationTestEndpoint):
    @pytest.fixture(autouse=True)
    def _patch_services(self, app: FastAPI):
        self._service_delete_mock = MagicMock(ServiceDeleteTest)
        app.dependency_overrides[
            ServiceDeleteTest
        ] = lambda: self._service_delete_mock

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "id",
        [
            UUID("f3e70682-d209-4cac-629f-6fbed82c07cd"),
            UUID("f7c1bd87-eda5-e709-d471-3d60c8a70639"),
            UUID("f7c1bd87-eda5-e709-d471-3d60c8a7063b"),
        ],
    )
    async def test_delete(self, id: UUID):
        """
        Test the DELETE method of the PartsController by creating a new part
        and verifying that it was added to the database.
        """
        response = await self._client.delete(
            f"/tests?id={id}",
        )

        assert response.status_code == 200
        assert response.json() == {"message": "Test deleted successfully"}
        self._service_delete_mock.delete_test.assert_called_once_with(id)


class TestTestPatch(BaseIntegrationTestEndpoint):
    @pytest.fixture(autouse=True)
    def _patch_services(self, app: FastAPI):
        self._service = MagicMock(ServiceUpdateTest)
        app.dependency_overrides[ServiceUpdateTest] = lambda: self._service

    @pytest.fixture
    def _setup_test(self, _patch_services):
        self._test = TestDomain(
            id=UUID("f3e70682-d209-4cac-629f-6fbed82c07cd"),
            part_id=UUID("7f411fed-1e70-e799-33a1-d1c2ad4ab155"),
            timestamp=datetime.datetime(2014, 5, 11, 10, 23, 44),
            successful=False,
            data={"type": "height", "priority": "2"},
        )

        self._service.update_data.return_value = self._test

    @pytest_asyncio.fixture
    async def _setup_response(self, setup_client, _setup_test):
        self._response = await self._client.patch(
            "/tests",
            json={
                "id": "f3e70682-d209-4cac-629f-6fbed82c07cd",
                "successful": True,
                "data": {"type": "height", "priority": "2"},
                "timestamp": "2014-05-11T10:23:44",
            },
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "test",
        [
            TestDomain(
                id=UUID("f3e70682-d209-4cac-629f-6fbed82c07cd"),
                part_id=UUID("7f411fed-1e70-e799-33a1-d1c2ad4ab155"),
                timestamp=datetime.datetime(2014, 5, 11, 10, 23, 44),
                successful=False,
                data={"type": "height", "priority": "2"},
            ),
            TestDomain(
                id=UUID("f7c1bd87-eda5-e709-d471-3d60c8a70639"),
                part_id=UUID("b0d9c2aa-8f83-7ef7-2746-0f22403d1f83"),
                timestamp=datetime.datetime(2018, 8, 18, 15, 5, 10),
                successful=True,
                data={"type": "height", "priority": "3"},
            ),
            TestDomain(
                id=UUID("f7c1bd87-eda5-e709-d471-3d60c8a7063b"),
                part_id=UUID("e8f6cf32-a25b-59fd-92e8-e269d12ecbc4"),
                timestamp=datetime.datetime(2020, 4, 9, 3, 53, 44),
                successful=False,
                data={"type": "design", "priority": "3"},
            ),
        ],
    )
    async def test_patch_content(self, test: TestDomain):
        """
        Test the DELETE method of the PartsController by creating a new part
        and verifying that it was added to the database.
        """
        self._service.update_data.return_value = test

        response = await self._client.patch(
            "/tests",
            json={
                "id": str(test.id),
                "successful": test.successful,
                "data": test.data,
                "timestamp": str(test.timestamp),
            },
        )
        assert response.json() == test.to_dict()

    async def test_patch_status(self, _setup_response):
        """
        Test the PATCH endpoint for updating the status of a test.
        """
        assert self._response.status_code == 200

    async def test_patch_side_effect(self, _setup_response):
        """
        Test the side effect of patching a resource.
        """
        self._service.update_data.assert_called_once()
