from datetime import datetime
from unittest.mock import patch
from uuid import UUID
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Database
from app.schemas import PartRegistrationDTO
from app.service import ServiceCreatePart
from app.session import Session
from app.unit_of_work import TestUnitOfWork


class BaseTestIntegrationService:
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
    def _setup_session(self):
        self._session = Session()

    @pytest.fixture(autouse=True)
    def unit_of_work(
        self,
        _setup_session,
        db_session: AsyncSession,
        reset_db: None,
        load_data: None,
    ):
        self._unit_of_work = TestUnitOfWork(
            self._session, Database(db_session)
        )


class TestServiceCreatePart(BaseTestIntegrationService):
    @pytest.fixture(autouse=True)
    def _setup_service(self, unit_of_work):
        self._service = ServiceCreatePart(self._unit_of_work)

    @pytest.mark.asyncio
    async def test_create_part(self):
        dto = PartRegistrationDTO(name="part_201")
        part_domain = await self._service.create_part(dto)

        assert part_domain.id == UUID("12345678123456781234567812345678")
        assert part_domain.name == "part_201"
        assert part_domain.modified_timestamp == datetime(2020, 1, 1)
