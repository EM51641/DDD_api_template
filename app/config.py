import os
from dataclasses import dataclass

from pydantic import PostgresDsn

database_uri = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_SERVER", "localhost"),
    path=f"/{os.getenv('POSTGRES_DB')}",
)


@dataclass(frozen=True)
class Settings:
    DATABASE_URI: str = database_uri
