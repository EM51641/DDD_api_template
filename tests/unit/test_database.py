from unittest.mock import Mock

from sqlalchemy.ext.asyncio import AsyncSession


def test_database_constructor():
    from app.database import Database

    db = Database(Mock(AsyncSession))
    assert isinstance(db.session, AsyncSession)
