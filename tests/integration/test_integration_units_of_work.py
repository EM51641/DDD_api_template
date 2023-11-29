import pytest
from uuid import UUID
import pytest_asyncio
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from datetime import datetime
from app.database import Database
from app.models import Part
from app.session import Session
from app.unit_of_work import TestUnitOfWork


class BaseIntegrationUOWTest:
    @pytest.fixture(autouse=True)
    def _setup_db(
        self, db_session: AsyncSession, reset_db: None, load_data: None
    ):
        self._db = Database(db_session)

    @pytest.fixture(autouse=True)
    def _setup_session(self):
        self._session = Session()

    @pytest_asyncio.fixture(autouse=True)
    async def _setup_test_db(self, engine: AsyncEngine):
        async with AsyncSession(engine, expire_on_commit=False) as db:
            self._test_db = db
            yield


class TestTestUnitOfWork(BaseIntegrationUOWTest):
    @pytest_asyncio.fixture(autouse=True)
    async def _remove_from_session(
        self,
        _setup_db,
        _setup_session,
    ):
        part_to_remove = select(Part).where(
            Part.id == UUID("e3e70682-c209-4cac-629f-6fbed82c07cd")
        )
        res = await self._db.session.execute(part_to_remove)
        self._session.remove(res.scalar_one())

    @pytest_asyncio.fixture(autouse=True)
    async def _add_to_session(
        self,
        _setup_db,
        _setup_session,
    ):
        part_to_add = Part(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            name="part_101",
            modified_timestamp=datetime(2022, 1, 1, 0, 0, 0),
        )
        self._db.session.add(part_to_add)

    @pytest.fixture(autouse=True)
    def _setup_unit_of_work(self):
        self._unit_of_work = TestUnitOfWork(db=self._db, session=self._session)

    @pytest.mark.asyncio
    async def test_save(self):
        """
        Test the add method of the TestUnitOfWork class.
        """
        await self._unit_of_work.save()

        res = await self._test_db.execute(
            text(
                "SELECT * FROM part where id = '00000000-0000-0000-0000-000000000001'"
            )
        )
        assert res.scalar_one()

        res = await self._db.session.execute(
            text(
                "SELECT * FROM part where id = 'e3e70682-c209-4cac-629f-6fbed82c07cd'"
            )
        )

        assert res.scalar() is None
