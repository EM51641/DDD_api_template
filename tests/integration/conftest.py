"""
This module contains fixtures for setting up and tearing
down the test environment.
"""
from datetime import datetime, timedelta
from typing import AsyncGenerator
from uuid import UUID
from fastapi import FastAPI
from pydantic import PostgresDsn
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)
import random
import os
from app.models import Base, Part, Test
from app.config import Settings
from app.main import FastApiManager


@pytest.fixture
def seed() -> int:
    """
    Add a seed
    """
    return 0


@pytest.fixture
def setup_base_sqlalchemy_class():
    """
    Setups a base SQLAlchemy class for testing.
    """
    from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
    from sqlalchemy import UUID as UUID_

    class FakeBaseEntity(DeclarativeBase):
        id: Mapped[UUID] = mapped_column(UUID_(as_uuid=True), primary_key=True)

    return FakeBaseEntity


@pytest.fixture
def settings() -> Settings:
    """
    Returns the test database settings.
    """
    if os.getenv("CI"):
        test_db_uri = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user="test",
            password="test",
            host="localhost",
            path="/test-db",
        )
    else:
        test_db_uri = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user="test",
            password="test",
            host="db-test",
            path="/test-db",
        )

    return Settings(test_db_uri)


@pytest.fixture
def app_manager(settings: Settings) -> FastApiManager:
    """
    Configures the application for testing.
    """
    fast_api_manager = FastApiManager(settings=settings)
    return fast_api_manager


@pytest_asyncio.fixture()
async def engine(settings: Settings):
    """
    Creates an async engine using the provided test database settings and yields it.
    After the engine is used, it is disposed of.
    """
    engine = create_async_engine(settings.DATABASE_URI)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(engine: AsyncEngine):
    """
    Context manager that provides a database session to the decorated coroutine.
    """
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


# Add fixtures to generate data:


@pytest.fixture
def part_entities(seed):
    """
    Generates a list of 100 Part entities with random UUIDs, names, and modified timestamps.

    Returns:
        list: A list of Part entities.
    """
    random.seed(seed)  # type: ignore
    stack = []
    for _ in range(100):
        id = UUID(int=random.getrandbits(128))
        name = f"Part {random.randint(0, 100)}"
        modified_timestamp = datetime(
            random.randint(2010, 2023),
            random.randint(1, 12),
            random.randint(1, 28),
            random.randint(0, 23),
            random.randint(0, 59),
            random.randint(0, 59),
        )
        part = Part(id=id, name=name, modified_timestamp=modified_timestamp)
        stack.append(part)
    return stack


@pytest.fixture
def test_entities(part_entities: list[Part], seed: int):
    """
    Generate a list of 1000 Test objects with random data.

    Args:
        part_entities (list[Part]): A list of Part objects to use for generating Test objects.

    Returns:
        list[Test]: A list of 1000 Test objects with random data.
    """
    random.seed(seed)  # type: ignore

    stack = []
    for _ in range(1000):
        id = UUID(int=random.getrandbits(128))
        part = part_entities[random.randint(0, len(part_entities) - 1)]
        timestamp = part.modified_timestamp + timedelta(
            days=random.randint(0, 365),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59),
        )
        successful = random.choice([True, False])
        data = {
            "type": random.choice(["quality", "weight", "height", "design"]),
            "priority": random.choice(["1", "2", "3"]),
        }
        test = Test(
            id=id,
            part_id=part.id,
            timestamp=timestamp,
            successful=successful,
            data=data,
        )
        stack.append(test)
    return stack


# Add fixtures to load data into the db:
@pytest_asyncio.fixture
async def load_parts(
    part_entities: list[Part], db_session: AsyncSession
) -> None:
    db_session.add_all(part_entities)
    await db_session.commit()


@pytest_asyncio.fixture
async def load_tests(
    test_entities: list[Test], db_session: AsyncSession
) -> None:
    db_session.add_all(test_entities)
    await db_session.commit()


@pytest.fixture
def load_data(load_parts: None, load_tests: None) -> None:
    return None


@pytest_asyncio.fixture
async def reset_db(engine: AsyncEngine) -> None:
    """
    Reinitialises the database by dropping all tables and recreating them.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def app(app_manager: FastApiManager, reset_db) -> FastAPI:
    """
    Sets up the FastAPI application for testing.
    """
    await app_manager.init_app()
    return app_manager.app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """
    Sets up the test client for the FastAPI application.
    """
    async with AsyncClient(app=app, base_url="http://test/api/v1") as client:
        yield client
