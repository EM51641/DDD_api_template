from datetime import datetime
from typing import Any
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Database
from app.domains import PartDomain, PartJson, TestDomain
from app.repository import PartRepository, TestRepository
from app.session import Session


class BaseIntegrationTest:
    @pytest.fixture(autouse=True)
    def _setup_db(
        self, db_session: AsyncSession, reset_db: None, load_data: None
    ):
        self._db = Database(db_session)

    @pytest.fixture(autouse=True)
    def _setup_session(self):
        self._session = Session()


class TestIntegrationPartRepository(BaseIntegrationTest):
    @pytest.fixture(autouse=True)
    def _setup_repository(self, _setup_db, _setup_session):
        self._repository = PartRepository(db=self._db, session=self._session)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "id, expected_name, expected_timestamp",
        [
            (
                UUID("e3e70682-c209-4cac-629f-6fbed82c07cd"),
                "Part 53",
                datetime(2010, 5, 17, 15, 25, 58),
            ),
            (
                UUID("f7c1bd87-4da5-e709-d471-3d60c8a70639"),
                "Part 61",
                datetime(2015, 10, 7, 16, 8, 18),
            ),
            (
                UUID("9e4d6e3c-1846-d424-c17c-627923c6612f"),
                "Part 32",
                datetime(2018, 12, 26, 19, 57, 9),
            ),
            (
                UUID("12e0c8b2-bad6-40fb-1948-8dec4f65d4d9"),
                "Part 87",
                datetime(2015, 8, 18, 3, 22, 27),
            ),
            (
                UUID("e9bb17bc-a3f2-c9bf-9c63-16b950f24455"),
                "Part 26",
                datetime(2018, 8, 15, 16, 16, 3),
            ),
            (
                UUID("ea7e9d49-8c77-8ea6-eb20-83e6ce164dba"),
                "Part 1",
                datetime(2011, 12, 27, 12, 45, 52),
            ),
            (
                UUID("004ae545-a011-6be5-ab0c-1681c8f8e3d0"),
                "Part 78",
                datetime(2017, 6, 8, 23, 20, 45),
            ),
            (
                UUID("eac1c14f-30e9-c5cc-101f-bcccded733e8"),
                "Part 72",
                datetime(2013, 4, 26, 4, 51, 34),
            ),
            (
                UUID("fe43c49e-1498-18d1-1759-edc372ae2244"),
                "Part 40",
                datetime(2018, 8, 4, 9, 35, 18),
            ),
        ],
    )
    async def test_find_id(
        self, id: UUID, expected_name: str, expected_timestamp: datetime
    ):
        part = await self._repository.find_by_id(id)
        assert part.id == id
        assert part.name == expected_name
        assert part.modified_timestamp == expected_timestamp

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "limit, offset, expected_data",
        [
            (
                10,
                0,
                [
                    PartDomain(
                        id=UUID("e3e70682-c209-4cac-629f-6fbed82c07cd"),
                        name="Part 53",
                        modified_timestamp=datetime(2010, 5, 17, 15, 25, 58),
                    ),
                    PartDomain(
                        id=UUID("f7c1bd87-4da5-e709-d471-3d60c8a70639"),
                        name="Part 61",
                        modified_timestamp=datetime(2015, 10, 7, 16, 8, 18),
                    ),
                    PartDomain(
                        id=UUID("9e4d6e3c-1846-d424-c17c-627923c6612f"),
                        name="Part 32",
                        modified_timestamp=datetime(2018, 12, 26, 19, 57, 9),
                    ),
                    PartDomain(
                        id=UUID("12e0c8b2-bad6-40fb-1948-8dec4f65d4d9"),
                        name="Part 87",
                        modified_timestamp=datetime(2015, 8, 18, 3, 22, 27),
                    ),
                    PartDomain(
                        id=UUID("e9bb17bc-a3f2-c9bf-9c63-16b950f24455"),
                        name="Part 26",
                        modified_timestamp=datetime(2018, 8, 15, 16, 16, 3),
                    ),
                    PartDomain(
                        id=UUID("ea7e9d49-8c77-8ea6-eb20-83e6ce164dba"),
                        name="Part 1",
                        modified_timestamp=datetime(2011, 12, 27, 12, 45, 52),
                    ),
                    PartDomain(
                        id=UUID("004ae545-a011-6be5-ab0c-1681c8f8e3d0"),
                        name="Part 78",
                        modified_timestamp=datetime(2017, 6, 8, 23, 20, 45),
                    ),
                    PartDomain(
                        id=UUID("eac1c14f-30e9-c5cc-101f-bcccded733e8"),
                        name="Part 72",
                        modified_timestamp=datetime(2013, 4, 26, 4, 51, 34),
                    ),
                    PartDomain(
                        id=UUID("fe43c49e-1498-18d1-1759-edc372ae2244"),
                        name="Part 40",
                        modified_timestamp=datetime(2018, 8, 4, 9, 35, 18),
                    ),
                    PartDomain(
                        id=UUID("552f233a-8c25-166a-1ff3-9849b4e1357d"),
                        name="Part 69",
                        modified_timestamp=datetime(2013, 10, 18, 18, 18, 28),
                    ),
                ],
            ),
            (
                5,
                5,
                [
                    PartDomain(
                        id=UUID("ea7e9d49-8c77-8ea6-eb20-83e6ce164dba"),
                        name="Part 1",
                        modified_timestamp=datetime(2011, 12, 27, 12, 45, 52),
                    ),
                    PartDomain(
                        id=UUID("004ae545-a011-6be5-ab0c-1681c8f8e3d0"),
                        name="Part 78",
                        modified_timestamp=datetime(2017, 6, 8, 23, 20, 45),
                    ),
                    PartDomain(
                        id=UUID("eac1c14f-30e9-c5cc-101f-bcccded733e8"),
                        name="Part 72",
                        modified_timestamp=datetime(2013, 4, 26, 4, 51, 34),
                    ),
                    PartDomain(
                        id=UUID("fe43c49e-1498-18d1-1759-edc372ae2244"),
                        name="Part 40",
                        modified_timestamp=datetime(2018, 8, 4, 9, 35, 18),
                    ),
                    PartDomain(
                        id=UUID("552f233a-8c25-166a-1ff3-9849b4e1357d"),
                        name="Part 69",
                        modified_timestamp=datetime(2013, 10, 18, 18, 18, 28),
                    ),
                ],
            ),
            (
                2,
                8,
                [
                    PartDomain(
                        id=UUID("fe43c49e-1498-18d1-1759-edc372ae2244"),
                        name="Part 40",
                        modified_timestamp=datetime(2018, 8, 4, 9, 35, 18),
                    ),
                    PartDomain(
                        id=UUID("552f233a-8c25-166a-1ff3-9849b4e1357d"),
                        name="Part 69",
                        modified_timestamp=datetime(2013, 10, 18, 18, 18, 28),
                    ),
                ],
            ),
            (
                3,
                3,
                [
                    PartDomain(
                        id=UUID("12e0c8b2-bad6-40fb-1948-8dec4f65d4d9"),
                        name="Part 87",
                        modified_timestamp=datetime(2015, 8, 18, 3, 22, 27),
                    ),
                    PartDomain(
                        id=UUID("e9bb17bc-a3f2-c9bf-9c63-16b950f24455"),
                        name="Part 26",
                        modified_timestamp=datetime(2018, 8, 15, 16, 16, 3),
                    ),
                    PartDomain(
                        id=UUID("ea7e9d49-8c77-8ea6-eb20-83e6ce164dba"),
                        name="Part 1",
                        modified_timestamp=datetime(2011, 12, 27, 12, 45, 52),
                    ),
                ],
            ),
        ],
    )
    async def test_find_all(
        self, limit: int, offset: int, expected_data: list[PartJson]
    ):
        data = await self._repository.find_all(limit, offset)
        assert data == expected_data


class TestIntegrationTestRepository(BaseIntegrationTest):
    @pytest.fixture(autouse=True)
    def _setup_repository(self, _setup_db, _setup_session):
        self._repository = TestRepository(db=self._db, session=self._session)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "id,expected_part_id,expected_timestamp,expected_success,expected_data",
        [
            (
                UUID("0641ff10-6866-bda9-f4d7-d57a923c6b6c"),
                UUID("3e37952d-30bc-ab0e-d857-010255d44936"),
                datetime(2021, 12, 22, 10, 42, 55),
                False,
                {"type": "height", "priority": "3"},
            ),
            (
                UUID("409d108c-84e2-ca17-0150-e8637021e6b0"),
                UUID("09018aee-6940-7be7-5a4f-4145fc98c279"),
                datetime(2017, 9, 15, 20, 46, 30),
                True,
                {"type": "weight", "priority": "3"},
            ),
            (
                UUID("b1e89782-e23d-2e90-2f9f-fc1ca0435943"),
                UUID("e8f6cf32-a25b-59fd-92e8-e269d12ecbc4"),
                datetime(2019, 11, 24, 10, 27, 29),
                True,
                {"type": "weight", "priority": "2"},
            ),
            (
                UUID("54c5b27d-e630-f8e3-286f-793daf2dd8f0"),
                UUID("0597aab6-14d3-0dbc-a0ac-f4c9658de17e"),
                datetime(2017, 11, 26, 12, 2, 15),
                True,
                {"type": "height", "priority": "2"},
            ),
            (
                UUID("16292b04-3072-b121-5996-c8b37fab391c"),
                UUID("642aad48-fcfc-fa81-b306-d70019d5f970"),
                datetime(2014, 7, 29, 16, 21, 4),
                False,
                {"type": "height", "priority": "1"},
            ),
            (
                UUID("89cf414b-a49e-36c5-728c-92053d4b89bc"),
                UUID("eac1c14f-30e9-c5cc-101f-bcccded733e8"),
                datetime(2014, 4, 10, 15, 58, 1),
                False,
                {"type": "quality", "priority": "3"},
            ),
            (
                UUID("42cea886-27c8-a86a-03fd-60b3afbd57df"),
                UUID("d1aa6c5e-3b01-9fcb-f96d-4403d48c93f3"),
                datetime(2011, 11, 14, 2, 28, 45),
                True,
                {"type": "design", "priority": "3"},
            ),
            (
                UUID("a72fabab-25ed-fea9-269d-c3b6c74093ac"),
                UUID("d360da69-6af7-9ad2-993e-c8c6e6b106e2"),
                datetime(2023, 11, 6, 10, 12, 5),
                True,
                {"type": "height", "priority": "2"},
            ),
            (
                UUID("44e8b777-03b2-67e2-1639-6b7a72720168"),
                UUID("f87f43fd-f606-2541-31d0-b6640589f877"),
                datetime(2021, 8, 18, 22, 2, 4),
                False,
                {"type": "height", "priority": "1"},
            ),
        ],
    )
    async def test_find_id(
        self,
        id: UUID,
        expected_part_id: UUID,
        expected_timestamp: datetime,
        expected_success: bool,
        expected_data: dict[Any, Any],
    ):
        part = await self._repository.find_by_id(id)
        assert part.id == id
        assert part.part_id == expected_part_id
        assert part.timestamp == expected_timestamp
        assert part.successful == expected_success
        assert part.data == expected_data

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "limit, offset, expected_data",
        [
            (
                10,
                100,
                [
                    TestDomain(
                        id=UUID("275f275c-c3f3-f74d-d386-1b58194665d3"),
                        part_id=UUID("1d7173e5-5bc7-fdeb-3123-4efe6e648043"),
                        timestamp=datetime(2024, 3, 20, 7, 7, 52),
                        successful=False,
                        data={"type": "design", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("7d718591-3fee-2fc7-2e2d-ffdff57b8a92"),
                        part_id=UUID("3d792fa1-2284-b7a4-47e7-f5938b5885ca"),
                        timestamp=datetime(2017, 8, 24, 18, 42, 44),
                        successful=False,
                        data={"type": "design", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("9c2e5562-4916-e844-e64d-dd918e9b185e"),
                        part_id=UUID("084fa819-052d-aad3-26c0-0984c734bb05"),
                        timestamp=datetime(2019, 7, 3, 8, 25, 33),
                        successful=False,
                        data={"type": "design", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("3b56735e-45c5-96d4-42d0-1ba3a2652c9e"),
                        part_id=UUID("9e4d6e3c-1846-d424-c17c-627923c6612f"),
                        timestamp=datetime(2019, 2, 25, 15, 47, 54),
                        successful=True,
                        data={"type": "weight", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("48d8b9ef-37d3-16a4-3faf-a2176a27241f"),
                        part_id=UUID("c4c536fb-1d4d-1180-4c6e-6fbb37fef6b5"),
                        timestamp=datetime(2015, 8, 23, 5, 15, 19),
                        successful=False,
                        data={"type": "quality", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("1e454241-45c1-90a8-a52b-a0ce627b585f"),
                        part_id=UUID("c4c536fb-1d4d-1180-4c6e-6fbb37fef6b5"),
                        timestamp=datetime(2015, 7, 6, 15, 42, 28),
                        successful=False,
                        data={"type": "weight", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("1095e497-3d79-8f0b-e6cd-3595d4f0d65d"),
                        part_id=UUID("a417956f-29ee-7f3d-0ff0-30b86238d0a0"),
                        timestamp=datetime(2013, 10, 29, 7, 23, 16),
                        successful=False,
                        data={"type": "design", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("cf4bb315-2325-4d81-2bdf-b7279501e917"),
                        part_id=UUID("f7c1bd87-4da5-e709-d471-3d60c8a70639"),
                        timestamp=datetime(2016, 7, 17, 8, 28, 41),
                        successful=True,
                        data={"type": "weight", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("82ae752f-2d40-76bc-f9cb-2ee827be0381"),
                        part_id=UUID("552f233a-8c25-166a-1ff3-9849b4e1357d"),
                        timestamp=datetime(2013, 12, 27, 1, 9, 26),
                        successful=False,
                        data={"type": "weight", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("3bd3147d-d0f0-c75d-21d3-2e24bb891746"),
                        part_id=UUID("71d04b0f-656f-a7e6-b5c0-3f6f94e4cc44"),
                        timestamp=datetime(2021, 11, 24, 21, 34, 25),
                        successful=True,
                        data={"type": "design", "priority": "1"},
                    ),
                ],
            ),
            (
                5,
                500,
                [
                    TestDomain(
                        id=UUID("3b3ec678-559a-5f6d-43f7-5e7356a62bec"),
                        part_id=UUID("004ae545-a011-6be5-ab0c-1681c8f8e3d0"),
                        timestamp=datetime(2018, 3, 2, 6, 49, 18),
                        successful=True,
                        data={"type": "design", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("e0db4322-f8b8-b8b5-863a-5de90aea39ec"),
                        part_id=UUID("402d0baf-878b-9f6b-57a1-cb712975d279"),
                        timestamp=datetime(2019, 10, 19, 22, 15, 31),
                        successful=False,
                        data={"type": "weight", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("8a6993de-7e10-b884-9271-c5463db11d61"),
                        part_id=UUID("d360da69-6af7-9ad2-993e-c8c6e6b106e2"),
                        timestamp=datetime(2024, 2, 26, 23, 43, 10),
                        successful=True,
                        data={"type": "quality", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("d95e1ab2-4ba7-4934-aceb-5b5af421e7e0"),
                        part_id=UUID("c4c536fb-1d4d-1180-4c6e-6fbb37fef6b5"),
                        timestamp=datetime(2015, 3, 14, 0, 44, 59),
                        successful=False,
                        data={"type": "quality", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("ae1c4447-c430-97a8-e212-335fdbb85991"),
                        part_id=UUID("ec62b2c8-2648-ee38-e074-05eb215663ab"),
                        timestamp=datetime(2023, 5, 4, 13, 5, 22),
                        successful=True,
                        data={"type": "quality", "priority": "1"},
                    ),
                ],
            ),
            (
                20,
                50,
                [
                    TestDomain(
                        id=UUID("993ec8c6-e6b1-06e2-8911-0af04a276dda"),
                        part_id=UUID("7f411fed-1e70-e799-33a1-d1c2ad4ab155"),
                        timestamp=datetime(2014, 12, 23, 14, 29, 50),
                        successful=True,
                        data={"type": "quality", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("2e9583ea-bda1-7da2-000f-c63de2a01335"),
                        part_id=UUID("0597aab6-14d3-0dbc-a0ac-f4c9658de17e"),
                        timestamp=datetime(2017, 11, 15, 2, 25, 2),
                        successful=True,
                        data={"type": "design", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("c5c14262-4d84-9ec5-d334-886ff164f9d8"),
                        part_id=UUID("1d7173e5-5bc7-fdeb-3123-4efe6e648043"),
                        timestamp=datetime(2024, 6, 15, 4, 31, 58),
                        successful=True,
                        data={"type": "weight", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("0e370526-5582-a3bd-d476-fe38babd4745"),
                        part_id=UUID("e9bb17bc-a3f2-c9bf-9c63-16b950f24455"),
                        timestamp=datetime(2019, 4, 19, 5, 25, 34),
                        successful=True,
                        data={"type": "weight", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("775e0ec3-9c9d-03f3-0901-8aee69407be7"),
                        part_id=UUID("16408169-a38d-8afc-fdd2-ed7af97ccc57"),
                        timestamp=datetime(2022, 9, 30, 0, 20, 33),
                        successful=True,
                        data={"type": "quality", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("a1457899-21f8-c156-9e0d-f45b992a34a1"),
                        part_id=UUID("a7c5cb87-9b8b-71a1-b38a-05fbf61164ce"),
                        timestamp=datetime(2022, 1, 8, 19, 3, 4),
                        successful=False,
                        data={"type": "weight", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("7d859725-c707-aef9-c6c3-744cc88e03b6"),
                        part_id=UUID("6b5f5241-f323-ca74-d344-749096fd35d0"),
                        timestamp=datetime(2014, 9, 16, 17, 26, 13),
                        successful=False,
                        data={"type": "quality", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("c9df7e44-4bdf-fa7d-9f3d-d894b6af98b2"),
                        part_id=UUID("3e37952d-30bc-ab0e-d857-010255d44936"),
                        timestamp=datetime(2021, 11, 19, 8, 13, 10),
                        successful=True,
                        data={"type": "weight", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("5f1ff97c-71cf-f814-645b-d776c838a145"),
                        part_id=UUID("4523dbbb-1eee-d219-0588-d91dfbe86a8e"),
                        timestamp=datetime(2010, 4, 17, 2, 56, 46),
                        successful=True,
                        data={"type": "quality", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("06d2ed7c-e6ac-9d8a-4160-ff927c7550f2"),
                        part_id=UUID("a417956f-29ee-7f3d-0ff0-30b86238d0a0"),
                        timestamp=datetime(2014, 5, 1, 4, 39, 58),
                        successful=True,
                        data={"type": "weight", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("e38690e7-e27a-c8e9-d1c3-d1bcc6be6432"),
                        part_id=UUID("d1aa6c5e-3b01-9fcb-f96d-4403d48c93f3"),
                        timestamp=datetime(2012, 6, 19, 4, 33, 39),
                        successful=False,
                        data={"type": "quality", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("6c0be55c-90e6-39e1-e44f-c3a96d0c62c3"),
                        part_id=UUID("6288e1a5-cc45-7821-98a6-416d1775336d"),
                        timestamp=datetime(2019, 6, 2, 18, 16, 58),
                        successful=False,
                        data={"type": "weight", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("725c2675-ca95-71e4-07dc-02b1f45da406"),
                        part_id=UUID("905c053b-25fd-acbe-7ce7-1b48fba52e59"),
                        timestamp=datetime(2021, 11, 1, 5, 33, 14),
                        successful=False,
                        data={"type": "height", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("5bf80676-1f12-a0e9-1201-1caa5a3da367"),
                        part_id=UUID("4c4b91fe-6c14-8fc6-9750-ca7e246cb09c"),
                        timestamp=datetime(2015, 2, 24, 2, 2, 34),
                        successful=True,
                        data={"type": "weight", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("24aeba79-e4b8-2987-98ba-0f0e120d7126"),
                        part_id=UUID("91b15f5d-e66c-d36e-68ef-8f5fae68690a"),
                        timestamp=datetime(2014, 11, 13, 19, 36, 25),
                        successful=True,
                        data={"type": "quality", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("eecb325b-064f-768d-b080-e0035e7f503c"),
                        part_id=UUID("6a677623-1ad1-daaa-ef8d-9ff015831fee"),
                        timestamp=datetime(2011, 11, 21, 8, 57, 30),
                        successful=True,
                        data={"type": "design", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("215203c7-421a-a15e-f58c-43ceb51d70d8"),
                        part_id=UUID("12e0c8b2-bad6-40fb-1948-8dec4f65d4d9"),
                        timestamp=datetime(2015, 12, 2, 14, 43, 57),
                        successful=False,
                        data={"type": "height", "priority": "3"},
                    ),
                    TestDomain(
                        id=UUID("97d01e70-2f1d-9bef-53b5-3b92a2cb5f38"),
                        part_id=UUID("6288e1a5-cc45-7821-98a6-416d1775336d"),
                        timestamp=datetime(2019, 6, 1, 22, 50, 11),
                        successful=True,
                        data={"type": "design", "priority": "1"},
                    ),
                    TestDomain(
                        id=UUID("390a9016-cdec-85da-200f-7753f217faac"),
                        part_id=UUID("8ef066d4-4279-b14d-ae55-cdff34ab18fd"),
                        timestamp=datetime(2016, 7, 14, 9, 10, 35),
                        successful=True,
                        data={"type": "height", "priority": "2"},
                    ),
                    TestDomain(
                        id=UUID("dc68d4fd-0bd7-696f-a9c7-2e7b6b770df1"),
                        part_id=UUID("3e37952d-30bc-ab0e-d857-010255d44936"),
                        timestamp=datetime(2022, 3, 7, 22, 39, 27),
                        successful=True,
                        data={"type": "weight", "priority": "2"},
                    ),
                ],
            ),
            (
                50,
                999,
                [
                    TestDomain(
                        id=UUID("0641ff10-6866-bda9-f4d7-d57a923c6b6c"),
                        part_id=UUID("3e37952d-30bc-ab0e-d857-010255d44936"),
                        timestamp=datetime(2021, 12, 22, 10, 42, 55),
                        successful=False,
                        data={"type": "height", "priority": "3"},
                    )
                ],
            ),
        ],
    )
    async def test_find_all(
        self, limit: int, offset: int, expected_data: list[TestDomain]
    ):
        data = await self._repository.find_all(limit, offset)
        assert data == expected_data
