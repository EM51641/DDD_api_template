from unittest.mock import Mock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import PartRepository, TestRepository
from app.session import Session
from app.unit_of_work import TestUnitOfWork


class TestTestUnitsOfWork:
    @pytest.fixture(autouse=True)
    def _setup_session(self):
        self._session = Mock(Session)

    @pytest.fixture(autouse=True)
    def _setup_db(self):
        self._db = Mock(AsyncSession)

    @pytest.fixture(autouse=True)
    def _patch_part_repository(self):
        with patch(
            "app.unit_of_work.PartRepository",
            return_value=Mock(PartRepository),
        ):
            yield

    @pytest.fixture(autouse=True)
    def _patch_test_repository(self):
        with patch(
            "app.unit_of_work.TestRepository",
            return_value=Mock(TestRepository),
        ):
            yield

    @pytest.fixture(autouse=True)
    def _setup_unit_of_work(self):
        self._uow = TestUnitOfWork(self._session, self._db)

    def test_constructor(self):
        assert self._uow.db == self._db
        assert self._uow.session == self._session
        assert isinstance(self._uow.part_repository, PartRepository)
        assert isinstance(self._uow.test_repository, TestRepository)
