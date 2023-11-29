from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, TypedDict
from uuid import UUID


class TestJson(TypedDict):
    id: str
    part_id: str
    timestamp: str
    successful: bool
    data: dict[Any, Any] | None


class PartJson(TypedDict):
    id: str
    name: str
    modified_timestamp: str


class BaseDomain(ABC):
    """
    Base class for Domain
    """

    def __init__(self, id: UUID) -> None:
        self._id = id

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the object, or None if the ID has not been set.
        """
        return self._id


class BaseTestDomain(BaseDomain):
    """
    Base class for TestDomain
    """

    def __init__(
        self,
        id: UUID,
        part_id: UUID,
        timestamp: datetime,
        successful: bool,
        data: dict[Any, Any] | None = None,
    ) -> None:
        super().__init__(id)
        self._part_id = part_id
        self._timestamp = timestamp
        self._successful = successful
        self._data = data

    @property
    @abstractmethod
    def part_id(self) -> UUID:
        """Not implemented yet"""

    @property
    @abstractmethod
    def timestamp(self) -> datetime:
        """Not implemented yet"""

    @property
    @abstractmethod
    def successful(self) -> bool:
        """Not implemented yet"""

    @property
    @abstractmethod
    def data(self) -> dict[Any, Any] | None:
        """Not implemented yet"""

    @abstractmethod
    def set_data(self, data: dict[Any, Any] | None) -> None:
        """Not implemented yet"""

    @abstractmethod
    def set_success_state(self, state: bool) -> None:
        """Not implemented yet"""

    @abstractmethod
    def set_timestamp(self, timestamp: datetime) -> None:
        """Not implemented yet"""

    @abstractmethod
    def to_dict(self) -> TestJson:
        """Not implemented yet"""


class TestDomain(BaseTestDomain):
    """A class representing a test domain.

    Attributes
    ----------
    part_id : UUID
        The ID of the part being tested.
    timestamp : datetime
        The timestamp of when the test was run.
    successful : bool
        Whether the test was successful or not.
    data : dict
        Any additional information about the test.
    """

    @property
    def part_id(self) -> UUID:
        """Getter for part_id

        Returns
        -------
        int
            The part_id of the Test
        """

        return self._part_id

    @property
    def timestamp(self) -> datetime:
        """Getter for timestamp

        Returns
        -------
        datetime
            The timestamp of the Test
        """

        return self._timestamp

    @property
    def successful(self) -> bool:
        """Getter for successful

        Returns
        -------
        bool
            The successful of the Test
        """

        return self._successful

    @property
    def data(self) -> dict[Any, Any] | None:
        """Getter for extra

        Returns
        -------
        dict[Any, Any]
            The additional data of the Test
        """

        return self._data

    def set_data(self, data: dict[Any, Any] | None) -> None:
        """Setter for extra

        Parameters
        ----------
        extra: dict[Any, Any]
            The extra data of the Test
        """

        self._data = data

    def set_success_state(self, state: bool) -> None:
        """Setter for successful

        Parameters
        ----------
        successful: bool
            The successful of the Test
        """

        self._successful = state

    def set_timestamp(self, timestamp: datetime) -> None:
        """Setter for timestamp

        Parameters
        ----------
        timestamp: datetime
            The timestamp of the Test
        """

        self._timestamp = timestamp

    def to_dict(self) -> TestJson:
        """Converts the Test to a dict

        Returns
        -------
        TestJson
            The Test as a dict
        """

        return {
            "id": str(self._id),
            "part_id": str(self._part_id),
            "timestamp": str(self._timestamp),
            "successful": self._successful,
            "data": self._data,
        }

    def __str__(self) -> str:
        return f"id={self._id}, part_id={self._part_id}, timestamp={self._timestamp}, successful={self._successful}, data={self._data}"  # noqa

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={repr(self._id)}, part_id={repr(self._part_id)}, timestamp={repr(self._timestamp)}, successful={repr(self._successful)}, data={repr(self._data)})"  # noqa

    def __eq__(self, value: object) -> bool:
        if isinstance(value, TestDomain):
            return (
                self._id == value._id
                and self.part_id == value.part_id
                and self.data == value.data
                and self.timestamp == value.timestamp
                and self.successful == value.successful
            )
        return False


class BasePartDomain(BaseDomain):
    def __init__(
        self,
        id: UUID,
        name: str,
        modified_timestamp: datetime,
    ) -> None:
        super().__init__(id)
        self._name = name
        self._modified_timestamp = modified_timestamp

    @property
    @abstractmethod
    def name(self) -> str:
        """Not implemented yet"""

    @property
    @abstractmethod
    def modified_timestamp(self) -> datetime:
        """Not implemented yet"""

    @abstractmethod
    def set_modified_timestamp(self, modified_timestamp: datetime) -> None:
        """Not implemented yet"""


class PartDomain(BasePartDomain):
    """A class representing a part domain.

    Attributes
    ----------
    name : str
        The name of the part.
    modified_timestamp : datetime
        The timestamp of when the part was last modified.
    """

    @property
    def name(self) -> str:
        """Getter for name

        Returns
        -------
        str
            The name of the Part
        """

        return self._name

    @property
    def modified_timestamp(self) -> datetime:
        """Getter for modified_timestamp

        Returns
        -------
        datetime
            The modified_timestamp of the Part
        """

        return self._modified_timestamp

    def set_modified_timestamp(self, modified_timestamp: datetime) -> None:
        """Setter for modified_timestamp

        Parameters
        ----------
        modified_timestamp: datetime
            The modified_timestamp of the Part
        """

        self._modified_timestamp = modified_timestamp

    def to_dict(self) -> PartJson:
        """Converts the Part to a dict

        Returns
        -------
        PartJson
            The Part as a dict
        """
        return {
            "id": str(self._id),
            "name": self._name,
            "modified_timestamp": str(self._modified_timestamp),
        }

    def __str__(self) -> str:
        return f"id={self._id}, name={self._name}, modified_timestamp={self._modified_timestamp}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={repr(self._id)}, name={repr(self._name)}, modified_timestamp={repr(self._modified_timestamp)})"  # noqa

    def __eq__(self, value: object) -> bool:
        if isinstance(value, PartDomain):
            return (
                self._id == value.id
                and self._name == value.name
                and self._modified_timestamp == value.modified_timestamp
            )
        return False
