"""
Module for database managers.
"""
from typing import AsyncGenerator

from app.database import Database, DatabaseApp

db_app = DatabaseApp()


async def get_db() -> AsyncGenerator[Database, None]:
    """
    Returns an asynchronous generator that yields a Database object.

    The Database object is created using the session_maker method of the db_app object.
    The generator ensures that the Database object is properly cleaned up after it is used.

    Yields:
        Database: A Database object.

    """
    db = Database(db_app.session_maker())
    try:
        yield db
    finally:
        await db.teardown_session()
