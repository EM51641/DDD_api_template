import os
from dataclasses import dataclass
from pydantic import PostgresDsn


database_uri = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.environ["POSTGRES_SERVER"],
    path=f"/{os.environ['POSTGRES_DB']}",
)


@dataclass(frozen=True)
class Settings:
    DATABASE_URI: str = database_uri
