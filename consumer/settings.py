import typing

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class NatsSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NATS_")

    server: str = "localhost:4222"
    subject: str = "glazboga.events"


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    user: str = "postgres"
    password: str = ""
    host: str = "localhost"
    database: str = "postgres"

    @computed_field  # type: ignor[misc]
    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.database}"


class Settings(BaseSettings):
    log_lvl: str = "debug"

    mq: NatsSettings = NatsSettings()
    db: PostgresSettings = PostgresSettings()


settings: typing.Final = Settings()
