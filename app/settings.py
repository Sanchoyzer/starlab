from enum import StrEnum, unique
from typing import Final

from pydantic import HttpUrl
from pydantic_settings import BaseSettings


@unique
class EnvType(StrEnum):
    DEV = 'dev'
    PROD = 'prod'


class Settings(BaseSettings):
    CI: bool = False
    ENV: EnvType = EnvType.DEV

    SPEC_VERSION: str = '0.1.0'
    SPEC_TITLE: str = 'My application'
    SPEC_URL_PREFIX: str = '/docs'

    SENTRY_DSN: HttpUrl | None = None

    PG_USER: str = 'postgres'
    PG_PASSWORD: str = 'postgres'
    PG_SERVER: str = 'localhost'
    PG_POST: int = 5432
    PG_DB_NAME: str = 'postgres'
    PG_POOL_SIZE: int = 5

    @property
    def pg_connection_string(self) -> str:
        user_info: Final[str] = f'{self.PG_USER}:{self.PG_PASSWORD}'
        server_info: Final[str] = f'{self.PG_SERVER}:{self.PG_POST}'
        return f'postgresql+asyncpg://{user_info}@{server_info}/{self.PG_DB_NAME}'


conf = Settings()
