from unittest.mock import Mock

import pytest

from app.models import Base
from app.session import Session, SessionEntity


class TestSession:
    @pytest.fixture(autouse=True)
    def _setup_session(self):
        self._session = Session()

    def test_constructor(self):
        assert self._session.session == []

    def test_add(self):
        entity = Mock(Base)
        self._session.add(entity)
        assert self._session.session == [
            SessionEntity(entity=entity, operation="add")
        ]

    def test_remove(self):
        entity = Mock(Base)
        self._session.remove(entity)
        assert self._session.session == [
            SessionEntity(entity=entity, operation="remove")
        ]
