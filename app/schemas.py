from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class PartRegistrationDTO(BaseModel):
    name: str


class PartChangeTimestampDTO(BaseModel):
    id: UUID
    modified_timestamp: datetime


class TestRegistrationDTO(BaseModel):
    part_id: UUID
    successful: bool
    data: dict[str, Any] | None


class TestUpdateDTO(BaseModel):
    id: UUID
    successful: bool | None
    data: dict[str, Any] | None
    timestamp: datetime | None
