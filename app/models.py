from datetime import datetime
from typing import Any
from uuid import UUID
from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    String,
    UUID as UUID_,
)
from sqlalchemy.orm import (
    declared_attr,
    DeclarativeBase,
    mapped_column,
    Mapped,
)


class Base(DeclarativeBase):
    """
    A class describing the declarative
    base of the model classes

    Attributes
    ----------
    id: int
        The primary key of a an instance of Base
    """

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        A declared attribute for __tablename__

        The __tablename__ for a classed derived from
        Base is its own name in lowercase by default.

        Returns
        -------
            str
                The class name in lowercase
        """
        return cls.__name__.lower()

    id: Mapped[UUID] = mapped_column(UUID_(as_uuid=True), primary_key=True)


class Part(Base):
    """A class describing Parts

    Attributes
    ----------
    id: UUID
        The primary key of a Part instance in the database
    name: str
        The name of a Part
    modified_timestamp: datetime.datetime
        The timestamp when Part was last modified
    """

    name: Mapped[str] = mapped_column(String)
    modified_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=False)
    )

    def __init__(
        self,
        id: UUID,
        name: str,
        modified_timestamp: datetime,
    ):
        self.id = id
        self.name = name
        self.modified_timestamp = modified_timestamp


class Test(Base):
    """
    A class describing Tests

    Attributes
    ----------
        part_id: int
            id of a Part the Test instance has been run on
        timestamp: datetime
            The timestamp when Test was ran
        succesful: bool
            The result of the Test
        data: dict[str, str]
            Additional json data of the Test
    """

    part_id: Mapped[UUID] = mapped_column(
        UUID_(as_uuid=True), ForeignKey(Part.id, ondelete="CASCADE")
    )
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    successful: Mapped[bool] = mapped_column(Boolean)
    data: Mapped[dict[Any, Any] | None] = mapped_column(JSON, nullable=True)

    def __init__(
        self,
        id: UUID,
        part_id: UUID,
        timestamp: datetime,
        successful: bool,
        data: dict[Any, Any] | None = None,
    ) -> None:
        self.id = id
        self.part_id = part_id
        self.timestamp = timestamp
        self.successful = successful
        self.data = data
