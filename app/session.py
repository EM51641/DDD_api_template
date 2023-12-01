"""
This module defines the Session Manager and related classes.
"""
from abc import ABC, abstractmethod
from typing import Literal, NamedTuple

from app.models import Base


class SessionEntity(NamedTuple):
    """
    Represents an enlisted entity in the session.
    """

    entity: Base
    operation: Literal["add", "remove"]


TSession = list[SessionEntity]


class SessionBase(ABC):
    """
    Abstract base class for Session Manager.
    """

    @property
    @abstractmethod
    def session(self) -> TSession:
        """Returns the session entities."""

    @abstractmethod
    def remove(self, item: Base) -> None:
        """Removes an entity from the session."""

    @abstractmethod
    def add(self, item: Base) -> None:
        """Adds an entity to the session."""


class Session(SessionBase):
    """
    Represents a session that stores entities and their operations.

    Attributes:
    ----
        _session (TSession): The list of session entities.

    Methods:
    ----
        session() -> TSession: Returns the session entities.
        add(item: Base) -> None: Adds an entity to the session.
        remove(item: Base) -> None: Removes an entity from the session.
    """

    _session: TSession

    def __init__(self) -> None:
        self._session = []

    @property
    def session(self) -> TSession:
        """Returns the session entities."""
        return self._session

    def add(self, item: Base) -> None:
        """
        Adds an entity to the session.

        Params:
        ----
           item (Base): The entity to be added.

        Returns:
        ----
           None.
        """
        session_entity = SessionEntity(entity=item, operation="add")
        self._session.append(session_entity)

    def remove(self, item: Base) -> None:
        """
        Removes an entity from the session.

        Params:
        ----
           item (Base): The entity to be removed.

        Returns:
        ----
           None.
        """
        session_entity = SessionEntity(entity=item, operation="remove")
        self._session.append(session_entity)
