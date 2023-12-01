"""
This module contains integration tests for the Test entity.

The Test entity is represented by a SQLAlchemy table with the following fields:
- id: int
- part_id: int
- successful: bool
- data: dict[Any, Any]
- timestamp: datetime

The tests ensure that the Test entity table is correctly defined and that its fields match the expected ones.
"""
from datetime import datetime
from typing import Any
from uuid import UUID

import pytest
from sqlalchemy import JSON
from sqlalchemy import UUID as UUID_
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Part, Test


class TestPartEntity:
    @pytest.fixture(autouse=True)
    def _fake_table(self, setup_base_sqlalchemy_class):
        """Creates a fake table for testing purposes.

        Args:
            setup_base_sqlalchemy_class: A SQLAlchemy base class.

        Returns:
            A SQLAlchemy table class.
        """

        class FakePartEntity(setup_base_sqlalchemy_class):
            __tablename__ = "part"

            name: Mapped[str] = mapped_column(String)
            modified_timestamp: Mapped[datetime] = mapped_column(DateTime())

        self._table = FakePartEntity

    def test_fields_number(self):
        """Test that the number of fields in the Part table is correct."""
        assert len(Part.__table__.columns) == 3  # type: ignore

    @pytest.mark.parametrize(
        "field",
        ["id", "name", "modified_timestamp"],
    )
    def test_fields(self, field: str) -> None:
        """
        Test that the fields of the fake table match the
        fields of the original table.

        Args:
            field (str): The name of the field to test.

        Returns:
            None
        """

        fake_table_field = self._table.__table__.columns[field]
        original_table_field = Part.__table__.columns[field]  # type: ignore

        assert repr(fake_table_field) == repr(original_table_field)

    def test_table_name(self):
        """Test that the table name is correctly set to 'part'."""
        assert Part.__tablename__ == "part"  # type: ignore


class TestTestEntity:
    @pytest.fixture(autouse=True)
    def _fake_table(self, setup_base_sqlalchemy_class):
        """Creates a fake table for testing purposes.

        Args:
            setup_base_sqlalchemy_class: A SQLAlchemy base class.

        Returns:
            A SQLAlchemy table class.
        """

        class FakeTestEntity(setup_base_sqlalchemy_class):
            __tablename__ = "test"

            part_id: Mapped[UUID] = mapped_column(
                UUID_(as_uuid=True), ForeignKey("part.id")
            )
            timestamp: Mapped[datetime] = mapped_column(DateTime())
            successful: Mapped[bool] = mapped_column(Boolean)
            data: Mapped[dict[Any, Any] | None] = mapped_column(
                JSON, nullable=True
            )

        self._table = FakeTestEntity

    def test_fields_number(self):
        """Test that the number of fields in the Test table is correct."""
        assert len(Test.__table__.columns) == 5  # type: ignore

    @pytest.mark.parametrize(
        "field",
        ["id", "part_id", "successful", "data", "timestamp"],
    )
    def test_fields(self, field: str) -> None:
        """Test that the fields of the fake table match the fields of the original table.

        Args:
            field (str): The name of the field to test.

        Returns:
            None
        """

        fake_table_field = self._table.__table__.columns[field]
        original_table_field = Test.__table__.columns[field]  # type: ignore

        assert repr(fake_table_field) == repr(original_table_field)

    def test_table_name(self):
        """Test that the table name is correctly set to 'test'."""
        assert Test.__tablename__ == "test"  # type: ignore
