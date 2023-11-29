import pytest
from unittest.mock import Mock, patch
from sqlalchemy import Result, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from app.database import Database
from app.domains import BaseDomain
from app.exceptions import NoEntityFoundError
from app.mappers import PartEntityDomainMapper, TestEntityDomainMapper
from app.models import Part, Test
from app.repository import BaseRepository, PartRepository, TestRepository
from app.session import Session


class BaseTestRepository:
    _repository: BaseRepository

    @pytest.fixture(autouse=True)
    def _patch_select(self):
        with patch(
            "app.repository.select",
            return_value=Mock(Select),
        ):
            yield

    def test_add(self):
        domain = Mock(BaseDomain)
        self._repository.add(domain)
        assert len(self._repository.session.session) == 1
        assert self._repository.session.session[0].operation == "add"

    @pytest.mark.asyncio
    async def test_remove(self):
        domain = Mock(BaseDomain)
        await self._repository.remove(domain)
        assert len(self._repository.session.session) == 1
        assert self._repository.session.session[0].operation == "remove"

    @pytest.mark.asyncio
    async def test_fail_modify(self):
        domain = Mock(BaseDomain)
        mock_result = Mock(Result)
        mock_result.scalar_one.side_effect = NoResultFound()
        self._repository.db.session.execute.return_value = mock_result

        with pytest.raises(NoEntityFoundError):
            await self._repository.modify(domain)

    @pytest.mark.asyncio
    async def test_fail_remove(self):
        domain = Mock(BaseDomain)
        mock_result = Mock(Result)
        mock_result.scalar_one.side_effect = NoResultFound()
        self._repository.db.session.execute.return_value = mock_result

        with pytest.raises(NoEntityFoundError):
            await self._repository.remove(domain)


class TestPartRepository(BaseTestRepository):
    @pytest.fixture(autouse=True)
    def _patch_mapper(self):
        with patch(
            "app.repository.PartEntityDomainMapper",
            return_value=Mock(PartEntityDomainMapper),
        ):
            yield

    @pytest.fixture(autouse=True)
    def _setup_repository(self):
        self._repository = PartRepository(
            db=Mock(Database, session=Mock(AsyncSession)), session=Session()
        )

    def test_custom_constructor(self):
        assert self._repository.entity_type == Part
        assert isinstance(self._repository.db, Database)
        assert isinstance(self._repository.mapper, PartEntityDomainMapper)
        assert isinstance(self._repository.session, Session)


class TestTestRepository(BaseTestRepository):
    @pytest.fixture(autouse=True)
    def _patch_mapper(self):
        with patch(
            "app.repository.TestEntityDomainMapper",
            return_value=Mock(TestEntityDomainMapper),
        ):
            yield

    @pytest.fixture(autouse=True)
    def _setup_repository(self):
        self._repository = TestRepository(
            db=Mock(Database, session=Mock(AsyncSession)),
            session=Session(),
        )

    def test_constructor(self):
        assert self._repository.entity_type == Test
        assert isinstance(self._repository.mapper, TestEntityDomainMapper)
        assert isinstance(self._repository.session, Session)
        assert isinstance(self._repository.db, Database)
